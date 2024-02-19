import requests
from flask import Blueprint, jsonify, redirect, request, session
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:3000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1'

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login')  # type:ignore
def login():
    print("This get pressed")
    scope = 'user-read-private user-read-email user-follow-read'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    print(auth_url)
    # this doesn't get redirect to /callback ????
    return jsonify({'auth_url': auth_url})


@auth_blueprint.route('/callback', methods=["GET", "POST"])  # type:ignore
def callback():
    # handle get and post method in here
    if request.method == 'POST':
        print("This is accessed")
        data = request.json
        code = data.get('code')
        if code:
            token_data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': REDIRECT_URI,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET
            }
            response = requests.post(TOKEN_URL, data=token_data)
            token_info = response.json()
            if 'access_token' in token_info:
                session['access_token'] = token_info['access_token']
                session['refresh_token'] = token_info['refresh_token']
                # Save the expiry time
                session['expires_at'] = datetime.now().timestamp() + \
                    token_info['expires_in']
                # Redirect or respond with the necessary information
                # or you can redirect to a different page
                print("get to /playlist in post callback")
                return redirect("/playlist")
            else:
                return jsonify({'error': 'Failed to retrieve access token'}), 400
        else:
            return jsonify({'error': 'No code provided'}), 400
    if request.method == 'GET':
        if 'error' in request.args:
            return jsonify({'error': request.args['error']})
        if 'code' in request.args:
            print(request)
            req_body = {
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': REDIRECT_URI,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET
            }
            response = requests.post(TOKEN_URL, data=req_body)
            token_info = response.json()
            session['access_token'] = token_info['access_token']
            session['refresh_token'] = token_info['refresh_token']
            # this coresponde to number of seconds the access_token will last
            session['expires_at'] = datetime.now().timestamp() + \
                token_info['expires_in']
            print("got to here for get /callback playlist")
            return redirect('/playlist')


@auth_blueprint.route('/playlist')  # type:ignore
def get_playlist():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f'Bearer {session['access_token']}'
    }

    response = requests.get(
        API_BASE_URL + '/me/following?type=artist', headers=headers)
    playlist = response.json()
    print("This is here It got to here")
    return jsonify(playlist)


@auth_blueprint.route('/refresh-token')  # type:ignore
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grand_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + \
            new_token_info['expires_in']
        return redirect('/playlist')


if __name__ == "__main__":
    auth_blueprint.run(host='0.0.0.0', debug=True)
