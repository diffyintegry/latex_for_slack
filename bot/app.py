#!/usr/bin/env python

import logging
import os

import requests
import json

from beepboop import resourcer
from beepboop import bot_manager

from slack_bot import SlackBot
from slack_bot import spawn_bot

logger = logging.getLogger(__name__)

from flask import Flask
from flask import request

_latex_url = 'http://latex.codecogs.com/png.latex?%5Cdpi%7B300%7D%20'

flaskApp=Flask(__name__)

@flaskApp.route("/slack/command", methods = ['GET','POST'])
def temp():
    logging.info(request.method)
    try:
        if request.method == 'POST':
            logging.info(request.form)
            token = request.form['token']
            text = request.form['text']
            logging.info(token + '  ' + text)
            payload = {
                        'response_type':'in_channel',
                        'text':'',
                        'attachments':[
                            {
                            'text':'<' + _latex_url + text + '>',
                            'unfurl': True,
                            }
                           ]
                        }
            headers = {'content-type':'application/json'}
            requests.post(request.form['response_url'], data = json.dumps(payload), headers = headers)
    except:
        logging.info('it failed!')
        logging.info(str(request.form))
    return ''



if __name__ == "__main__":
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=log_level)

    slack_token = os.getenv("SLACK_TOKEN", "")
    port = os.getenv("PORT","8080")

    logging.info("token: {}".format(slack_token))
    logging.info("port: {}".format(port))
    flaskApp.run(host = '0.0.0.0', port=port)
    

    if slack_token == "":
        logging.info("SLACK_TOKEN env var not set, expecting token to be provided by Resourcer events")
        slack_token = None
        botManager = bot_manager.BotManager(spawn_bot)
        res = resourcer.Resourcer(botManager)
        res.start()
    else:
        # only want to run a single instance of the bot in dev mode
        bot = SlackBot(slack_token)
        bot.start({})
