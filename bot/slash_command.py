import os
import base64
import requests
import json
import logging

from imgurpython import ImgurClient

logger = logging.getLogger(__name__)


_latex_url = 'http://chart.apis.google.com/chart?cht=tx&chl={latex}'


def handle_images(request, latexString):
    ''' takes a latex string and uploads to imgur for the image
    '''
    imgurClientID = request.headers['Bb-Config-Imclid']
    imgurSecret = request.headers['Bb-Config-Imsec']
    logger.info(imgurClientID + "...." + imgurSecret + ' ...')

    imgur = ImgurClient(imgurClientID, imgurSecret)
    latexImageDownload = _latex_url.format(latex = latexString.replace(' ',''))
    latexImage = requests.get(latexImageDownload).content
    data = {
            'image': base64.b64encode(latexImage),
            'type': 'base64',
            }
    imageData = imgur.make_request('POST','upload',data,True)
    latexImageLocation = imageData['link']
    return latexImageLocation    


def process_request(request):
    correctToken = os.getenv('SLACK_VERIFY_TOKEN','')

    if request.method == 'POST' and request.form['token'] == correctToken:
        logger.info(str(request.form))
        text = request.form['text']
        logger.info(str(request.form))
        image = handle_images(request, text)
        payload = {
                    'response_type':'in_channel',
                    'username':request.form['user_name'],
                    'attachments':[
                        {
                        'text': text,
                        'fallback': text,
                        'image_url': image,
                        }
                       ]
                    }
        logger.info(str(payload))
        headers = {'content-type':'application/json'}
        requests.post(request.form['response_url'], data = json.dumps(payload), headers = headers)



