#!flask/bin/python
import os
import hmac
import requests
import base64
import hashlib
import json

from slackeventsapi import SlackEventAdapter
from slack import WebClient

from flask import Flask, jsonify, request

app = Flask(__name__)

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events", app)

# Create a SlackClient for your bot to use for Web API requests
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_client = WebClient(slack_bot_token)


# Super simple. Slack pings with a request object,
# hit the webhook with the message that was sent
@app.route('/anon', methods=['POST'])
def anon():
    slack_client.chat_postMessage(channel=request.form['channel_id'], text=request.form['text'])
    return '', 200


# Example responder to greetings
@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    message = event_data["event"]

    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is None and "hi" in message.get('text'):
        channel = message["channel"]
        message = "Hello <@%s>! :tada:" % message["user"]
        slack_client.chat_postMessage(channel=channel, text=message)


# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    error_message = "Sorry, something went wrong and I couldn't post that message. Try again in a second."
    slack_client.chat_postMessage(channel=request.form['channel_id'], text=error_message)

if __name__ == '__main__':
    app.run()