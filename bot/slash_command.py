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
    return _latex_url.format(latex=latexString.replace(' ',''))


def process_request(request):
    correctToken = os.getenv('SLACK_VERIFY_TOKEN','')

    if request.method == 'POST' and request.form['token'] == correctToken:
        logger.info(str(request.form))
        text = request.form['text']
        logger.info(str(request.form))
        image = handle_images(request, text)
        payload = {
                    'response_type':'in_channel',
                    'text': text,
                    'username': 'latexbot',
                    'attachments':[
                        {
                        'fallback_text': text,
                        'image_url': image,
                        }
                       ]
                    }
        headers = {'content-type':'application/json'}
        requests.post(request.form['response_url'], data = json.dumps(payload), headers = headers)



