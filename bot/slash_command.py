import os
import base64
import requests
import json
import logging
from imgurpython import ImgurClient

logger = logging.getLogger(__name__)
_latex_url = 'http://chart.apis.google.com/chart?cht=tx&chl={latex}'

def get_usericon(slackRequest):
    '''returns the requesting user's icon so bot can use it
    '''
    api_token = slackRequest.headers['Bb-Slackbotaccesstoken']
    userid = slackRequest.form['user_id']
    url = 'https://slack.com/api/users.info'
    resp = requests.get(url, params={'token': api_token, 'user': userid})
    logger.info('Response JSON: %s' % resp.json())
    user_profile = resp.json()['user']['profile']
    logger.info('User Profile: %s' % user_profile)
    icon = user_profile['image_48']
    return icon

def handle_images(slackRequest, latexString):
    ''' takes a latex string and uploads to imgur for the image
    '''
    imgurClientID = slackRequest.headers['Bb-Config-Imclid']
    imgurSecret = slackRequest.headers['Bb-Config-Imsec']
    logger.info(imgurClientID + '....' + imgurSecret + ' ...')

    imgur = ImgurClient(imgurClientID, imgurSecret)
    latexImageDownload = _latex_url.format(latex = latexString.replace(' ','').replace('+','%2B'))
    latexImage = requests.get(latexImageDownload).content
    data = {
            'image': base64.b64encode(latexImage),
            'type': 'base64',
            }
    imageData = imgur.make_request('POST','upload',data,True)
    latexImageLocation = imageData['link']
    return latexImageLocation    


def payload_maker(slackRequest):
    ''' Delivers the payload depending on whether the webhooks has been set up or not
    '''
    webhooksURL = slackRequest.form['response_url']
    text = slackRequest.form['text']
    image = handle_images(slackRequest, text)
    payload = {
                'response_type': 'in_channel',
                'text': '/latex %s' % text,
                'attachments': [
                    {
                    'text': ' ',
                    'fallback': text,
                    'image_url': image,
                    }
                   ]
                }
    if 'Bb-Config-Webhooks' in slackRequest.headers and slackRequest.headers['Bb-Config-Webhooks']:
        webhooksURL = slackRequest.headers['Bb-Config-Webhooks']
        username = slackRequest.form['user_name']
        icon = get_usericon(slackRequest)
        channel = slackRequest.form['channel_id']
        payload.update({
                        'channel': channel,
                        'username': username,
                        'icon_url': icon,
                        })
    return webhooksURL, payload
        
                        
        

def process_request(slackRequest):
    correctToken = os.getenv('SLACK_VERIFY_TOKEN','')
    if slackRequest.method == 'POST' and slackRequest.form['token'] == correctToken:
        # data logging
        logger.info('POST form: %s' % slackRequest.form)
        logger.info('POST headers: %s' % slackRequest.headers)
        # data collection
        url, payload = payload_maker(slackRequest)
        logger.info(str(payload))
        headers = {'content-type':'application/json'}
        requests.post(url, data = json.dumps(payload), headers = headers)


