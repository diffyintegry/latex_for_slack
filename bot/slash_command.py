import os
import base64
import requests
import json
import logging

from imgurpython import ImgurClient

logger = logging.getLogger(__name__)


_latex_url = 'http://latex.codecogs.com/png.latex?%5Cdpi%7B300%7D%20'


def handle_images(latexString):
    ''' takes a latex string and uploads to imgur for the image
    '''
    imgurClientID = os.getenv('IMCLID','notatoken')
    imgurSecret = os.getenv('IMSEC','notatokeneither')
    logger.info(imgurClientID + "...." + imgurSecret + ' ...')

    imgur = ImgurClient(imgurClientID, imgurSecret)
    latexImageDownload = _latex_url + latexString.replace(' ','')
    latexImage = requests.get(latexImageDownload).content
    data = {
            'image': base64.b64encode(latexImage),
            'type': 'base64',
            }
    imageData = imgur.make_request('POST','upload',data,True)
    latexImageLocation = imageData['link']
    return latexImageLocation



def get_client_and_secret(request):
    ''' goes into headers and gets stuff
    '''
    



def process_request(request):
    correctToken = os.getenv('SLACK_VERIFY_TOKEN','')

    if request.method == 'POST' and request.form['token'] == correctToken:
        logger.info(str(request.form))
        try:
            logger.info(str(request.headers))
        except:
            logger.info(str(request.header))
        text = request.form['text']
        image = handle_images(text)
        payload = {
                    'response_type':'in_channel',
                    'text':'',
                    'attachments':[
                        {
                        'text': '<%s|Your LaTeX image!>' % image,
                        'unfurl_media': True,
                        'unfurl_link': True,
                        }
                       ]
                    }
        headers = {'content-type':'application/json'}
        requests.post(request.form['response_url'], data = json.dumps(payload), headers = headers)



