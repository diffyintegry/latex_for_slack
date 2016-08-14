import json
import logging
import re
import os

logger = logging.getLogger(__name__)


class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        elif event_type in ('add_resource', 'update_resource'):
            # new resourced added
            logging.info(str(event['resource']))
            if 'IMCLID' in event['resource']:
                key = 'IMCLID'
                value = event['resource']['IMCLID']
            elif 'IMSEC' in event['resource']:
                key = 'IMSEC'
                value = event['resource']['IMSEC']
            else:
                key = 'THISISAGARBAGEVARIABLE'
                value = 'IAMGARBAGE'
            os.environ[key] = value
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself
        try:
            if not self.clients.is_message_from_me(event['user']):

                msg_txt = event['text']
            
                if event['text'][:5] == 'latex':
		    latex_string = event['text'][6:]
                    self.msg_writer.render_latex(event['channel'], latex_string)
	except:
            pass
