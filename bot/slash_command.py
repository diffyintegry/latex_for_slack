import os
import base64
import requests
import json
import logging
from imgurpython import ImgurClient

logger = logging.getLogger(__name__)
_latex_url = 'http://chart.apis.google.com/chart?cht=tx&chl={latex}'


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


def process_request(slackRequest):
    correctToken = os.getenv('SLACK_VERIFY_TOKEN','')
    if slackRequest.method == 'POST' and slackRequest.form['token'] == correctToken:
        # data logging
        logger.info('POST form: %s' % slackRequest.form)
        logger.info('POST headers: %s' % slackRequest.headers)
        # data collection
        text = slackRequest.form['text']
        image = handle_images(slackRequest, text)
        webhooksURL = slackRequest.headers['Bb-Config-Webhooks']
        username = slackRequest.form['user_name']
        #TODO: implement user avatar

        channel = slackRequest.form['channel_id']
        payload = {
                    'response_type': 'in_channel',
                    'username': username,
                    'channel': channel,
                    'attachments': [
                        {
                        'text': ' ',
                        'fallback': text,
                        'image_url': image,
                        }
                       ]
                    }
        logger.info(str(payload))
        headers = {'content-type':'application/json'}
        requests.post(webhooksURL, data = json.dumps(payload), headers = headers)


