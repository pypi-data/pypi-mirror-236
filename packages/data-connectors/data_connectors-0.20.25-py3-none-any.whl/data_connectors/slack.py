import os
import json
import pendulum
import requests


class Slack:

    """
    Pass in workspace as a Slack token to send 
    messages to channels using plain requests
    """

    def __init__(self, workspace):
        self.TOKEN = os.getenv(workspace)
        self.div = "─────────────────────"

    @staticmethod
    def slackify(message):
        return f'```{message}```'

    def send_message(self, channel, message, blocks=None):
        message += f'\n{self.div}'

        response = requests.post("https://slack.com/api/chat.postMessage",
                             data={'token': self.TOKEN,
                                   'channel': channel,
                                   'text': message,
                                   'blocks': json.dumps(blocks) if blocks else None}).json()

        if not response['ok']:
            print(f"Invalid response. Error: {response['error']}")
        else:
            return response

    def send_file(self, channels, comment, filename):

        response = requests.post("https://slack.com/api/files.upload",
                             data={'token': self.TOKEN,
                                   'channels': channels,
                                   'initial_comment': comment},
                             files={'file': open(filename, 'rb')}).json()
        self.send_message(channel=channels, message='')

        if not response['ok']:
            print(f"Invalid response. Error: {response['error']}")
        else:
            return response

    def notify_yourself(self, message):

        now = pendulum.now(tz="Asia/Singapore").strftime('%Y-%m-%d %H:%M:%S %p')

        self.send_message(
            channel="UCFNX4DQ9",
            message=f"{now} - {message}"
        )