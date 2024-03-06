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


@auth_blueprint.route('/login')
def login():
    print(request.args.get('code'))
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
    return jsonify({'auth_url': auth_url})


@auth_blueprint.route('/callback', methods=['POST'])
def callback():
    content = request.json
    code = content['code']
    print(code)
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(url=TOKEN_URL, data=token_data)
    tokens = response.json()
    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')
    expires_in = tokens.get('expires_in')
    print(f"This is access token {access_token}")
    # expires_in = tokens.get('expires_in')
    session['access_token'] = access_token
    print(f"This is access token in session {session['access_token']}")
    session['refresh_token'] = refresh_token
    session['expires_at'] = datetime.now().timestamp() + expires_in
    # The rest of the token exchange logic as in your '/callback' route
    # Instead of returning "Authentication Successful!", return the tokens or a success status
    return jsonify({"success": True, "access_token": access_token})


@auth_blueprint.route('/follow-artist')  # type:ignore
def get_artists():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(
        API_BASE_URL + '/me/following?type=artist', headers=headers)
    playlist = response.json()
    return jsonify(playlist)


@auth_blueprint.route('/follow-playlists')  # type:ignore
def get_playlist():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(
        API_BASE_URL + '/me/playlists', headers=headers)
    playlist = response.json()
    return jsonify(playlist.get('items', []))


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
