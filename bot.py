import slack
import os
from pathlib import Path
from dotenv import load_dotenv 
import ssl
from flask import Flask 
from slackeventsapi import SlackEventAdapter 

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
ssl._create_default_https_context = ssl._create_unverified_context
app = Flask(__name__)
test_channel = 'C02RZHXAGUX'

slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])


@slack_event_adapter.on('member_joined_channel')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    welcome_message = """:tada: Welcome <@{}> to the Harness Community! :tada:
            
            Our goal is to help you get up and running and help you with anything you need. Please introduce yourself in the #intro-yourself channel and tell us what you are currently working on! 
            Some important information to help you get the most out of our community: 

            :question: <https://discourse.drone.io/t/how-to-ask-for-help/3483 | How to ask Questions>

            :meetup: <https://www.meetup.com/harness/ | Upcoming Events>

            :teamwork: Meet the team

            :memo: CoC violation form

            :telephone_receiver: You have a question, comment, or an idea?  <https://calendly.com/marie-antons/harness-community | Book a meeting with me>


    We are so happy to have you here, 
    Marie
        
        """.format(user_id)

    if channel_id == test_channel:
     client.chat_postMessage(channel=user_id, text= welcome_message)


if __name__ == "__main__":
    app.run(debug=True)