import requests
import pandas as pd
from flask import Blueprint, jsonify, redirect, request, session, Flask
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
import os
import json
import time


load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID") # see README in this folder for how to set these
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:3000/callback' # make sure to set this as the redirect uri in the spotify dashboard

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1'

# MILLION_PLAYLIST_DATASET = '/Users/alex/Documents/AU23/CSE 5914 Senior Project/spotify_million_playlist_dataset/data/mpd.slice.0-999.json' #absolute pathing

# df = pd.read_json(MILLION_PLAYLIST_DATASET)
# print(df)
# with open(MILLION_PLAYLIST_DATASET, 'r') as file:
#     data = json.load(file)
# we're now ready to party

app = Flask(__name__)
app.secret_key = CLIENT_SECRET
auth_blueprint = Blueprint('auth', __name__)
auth_blueprint.secret_key = CLIENT_SECRET

@auth_blueprint.route('/spotify')
def spotify():
    return {'number': 2}


@auth_blueprint.route('/login')  # type:ignore
def login():
    print("This is the print being run")
    scope = 'user-read-private user-read-email user-follow-read'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return jsonify({'auth_url': auth_url})


@auth_blueprint.route('/callback')  # type:ignore
def callback():
    print("This is being called")
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
        return redirect('/extract-features')

@auth_blueprint.route('/extract-features')  # type:ignore
def extract_features():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    print("This is the header")
    print(headers)
    
    # artists_extracted = 'artists-extracted.csv'
    # fieldnames = list(json_objects[0].keys())
    
    # 1000 playlists per file
    # for i in range(1000):
    #     for j in range(data['playlists'][i]['num_tracks']):
    #         print("we are on "+ str(i) + " "+ str(j))
    #         print(data['playlists'][i]['tracks'][j]['artist_uri'])
    #         response = requests.get(
    #             API_BASE_URL + '/artists/' + data['playlists'][i]['tracks'][j]['artist_uri'].split(':', 2)[2], headers=headers)
    #         artist = response.json()
    #         print(artist)
    #         print()
    #         time.sleep(5)
    #         response = requests.get(
    #             API_BASE_URL + '/tracks/' + data['playlists'][i]['tracks'][j]['track_uri'].split(':', 2)[2], headers=headers)
    #         artist = response.json()
    #         print(artist)
    #         print()
    #         print()
    #         print()
    #         time.sleep(5)


    # response = requests.get(
    #     API_BASE_URL + '/me/following?type=artist', headers=headers)
    # playlist = response.json()
    return None


@auth_blueprint.route('/playlist')  # type:ignore
def get_playlist():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    print("This is the header")
    print(headers)

    response = requests.get(
        API_BASE_URL + '/me/following?type=artist', headers=headers)
    playlist = response.json()
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

app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
