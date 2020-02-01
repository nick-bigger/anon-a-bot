#!flask/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Super simple. Slack pings with a request object,
# respond with a 200 and the text that was sent
@app.route('/anon', methods=['POST'])
def anon():
    return request.form['text'], 200


if __name__ == '__main__':
    app.run()