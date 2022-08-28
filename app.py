import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'ACfd335f7fcadcecc3e16fe8269f01b156'
    TWILIO_SYNC_SERVICE_SID = 'IS973579e7affd7225fa01d7f0bea01d2c'
    TWILIO_API_KEY = 'SKb5fe1d0fa634d6a939f96e5a6e92d225'
    TWILIO_API_SECRET = 'dAFBwFr7Yfp9bB5jeVnRYCag94Zjs3q3'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# A function to download text and store it in text file
@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad = request.form['text']
    with open('workfile.txt', 'w') as f:
        f.write(text_from_notepad)

    path_to_store_txt = "workfile.txt"

    return send_file(path_to_store_txt, as_attachment=True)


if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
