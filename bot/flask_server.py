#!/usr/bin/env python

import logging
import os


from flask import Flask
from flask import request

import slash_command

logger = logging.getLogger(__name__)

flaskApp = Flask(__name__)
    


@flaskApp.route('/slack/command', methods = ['GET','POST'])
def temp():
    try:
        slash_command.process_request(request)
    except Exception as e:
        logging.info('We failed! problem was\n%s' % e)
    return ''




if __name__ == '__main__':
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                         level=log_level)
    port = os.getenv('PORT','8080') 
    flaskApp.run(host='0.0.0.0', port=port)
    

