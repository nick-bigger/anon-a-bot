#!flask/bin/python
import os
import requests
import json
import hmac
import hashlib
import base64

from flask import Flask, jsonify, request

app = Flask(__name__)

# Super simple. Slack pings with a request object,
# hit the webhook with the message that was sent
@app.route('/anon', methods=['POST'])
def anon():
    if request_is_valid(request) and 'ANONYMOUS_SLACK_WEBHOOK_URL' in os.environ:
        data = {'text':request.form['text']}
        requests.post(url=os.environ['ANONYMOUS_SLACK_WEBHOOK_URL'], data=json.dumps(data))

        return '', 200

    return '', 401


def request_is_valid(request):
    request_body = request.get_data(as_text=True)
    timestamp = request.headers['X-Slack-Request-Timestamp']
    sig_basestring = ('v0:' + timestamp + ':' + request_body).encode("UTF-8")

    slack_signature = request.headers['X-Slack-Signature']
    slack_signing_secret = bytes(os.environ['SLACK_SIGNING_SECRET'], encoding="UTF-8")

    dig = hmac.new(slack_signing_secret, msg=sig_basestring, digestmod=hashlib.sha256).digest() 
    my_signature = 'v0=' + base64.b64encode(dig).decode()

    return hmac.compare_digest(my_signature, slack_signature)

if __name__ == '__main__':
    app.run()