#!flask/bin/python
import os
import requests
import json

from flask import Flask, jsonify, request

app = Flask(__name__)

# Super simple. Slack pings with a request object,
# hit the webhook with the message that was sent
@app.route('/anon', methods=['POST'])
def anon():
    if 'ANONYMOUS_SLACK_WEBHOOK_URL' in os.environ:
        data = {'text':request.form['text']}
        requests.post(url=os.environ['ANONYMOUS_SLACK_WEBHOOK_URL'], data=json.dumps(data))
    
    return '', 200


if __name__ == '__main__':
    app.run()