from flask import Flask, request, jsonify
from flask_cors import CORS
import auth
import home
import sys
import pandas as pd
import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials
import yaml
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import regex
from flask import Flask, request, jsonify
from flask_cors import CORS
import auth
import home
import requests
import sys

import pandas as pd
import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials
import yaml
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import regex
from flask import Flask, request, jsonify
import pickle  # Import pickle for loading the tokenizer
# from tensorflow.keras.models import load_model  # Import load_model to load your trained model
# from tensorflow.keras.preprocessing.sequence import pad_sequences

song_recommendations = pd.read_csv('test.csv')

sys.path.insert(0, 'Datasets')
app = Flask(__name__)
CORS(app)
app.secret_key = "dwasdwahdskajwdk"
app.register_blueprint(auth.auth_blueprint)
app.register_blueprint(home.home_blueprint)

@app.route('/display_reccommendations', methods=['GET'])
def get_recommendations():
    recommendations_json = song_recommendations.to_dict(orient='records')
    return jsonify(recommendations_json)

@app.route('/process_playlist', methods=['POST'])
def process_playlist():
    playlist_uri = request.json['playlist_uri']
    print("Received playlist URI:", playlist_uri)
    song_names, artist_names, song_uri = getRecs(playlist_uri)
    
    #return jsonify(song_names)
    songs_with_artists = [f"{song} - {artist}" for song, artist in zip(song_names, artist_names)]
    return jsonify(songs_with_artists)

    song_names, artist_names = getRecs(playlist_uri)
    
    #return jsonify(song_names)
    songs_with_artists = [f"{song} - {artist}" for song, artist in zip(song_names, artist_names)]
    return jsonify(songs_with_artists)

def getRecs(playlist_uri):

    # Open the spotify api credentials
    stream= open("spotify.yaml")
    spotify_details = yaml.safe_load(stream)
    client_id = spotify_details['client_id']
    client_secret = spotify_details['client_secret']

    def get_IDs (user, playlist_id):
        track_ids = []
        artist_id = []
        playlist=sp.user_playlist(user, playlist_id)
        for item in playlist['tracks']['items']:
            track=item['track']
            track_ids.append(track['id'])
            artist=item['track']['artists']
            artist_id.append(artist[0]['id'])
        return track_ids,artist_id

    # Read in the processed data
    df=pd.read_csv('1M_unique_processed_data.csv')

    # Create the authentication manager and connect to the spotify client
    auth_manager = SpotifyClientCredentials(client_id=client_id,
                                            client_secret=client_secret)
    sp = spotipy.client.Spotify(auth_manager=auth_manager)

    # Get the features for the users songs contained within the seed playlist
    track_ids,artist_id = get_IDs('Steven', playlist_uri) 
    artist_id_uni=list(set(artist_id))
    track_ids_uni=list(set(track_ids))

    audio_features=pd.DataFrame()
    track_=pd.DataFrame()
    artist_=pd.DataFrame()

    # Audio features
    for i in tqdm(range(0,len(track_ids_uni),25)):
        try:
            track_feature = sp.audio_features(track_ids_uni[i:i+25])
            track_df = pd.DataFrame(track_feature)
            audio_features=pd.concat([audio_features,track_df],axis=0)
        except Exception as e:
            print(e)
            continue

    # Track features
    for i in tqdm(range(0,len(track_ids_uni),25)):
        try:
            track_features = sp.tracks(track_ids_uni[i:i+25])
            for x in range(25):
                track_pop=pd.DataFrame([track_ids_uni[i+x]],columns=['track_uri'])
                track_pop['Track_release_date']=track_features['tracks'][x]['album']['release_date']
                track_pop['Track_pop'] = track_features['tracks'][x]["popularity"]
                track_pop['track_name']=track_features['tracks'][x]['name']
                track_pop['artist_uri']=track_features['tracks'][x]['artists'][0]['id']
                track_pop['album_uri']=track_features['tracks'][x]['album']['id']
                track_pop['album_name'] = track_features['tracks'][x]['album']['name']
                track_pop['artist_name'] = track_features['tracks'][x]['artists'][0]['name']
                track_=pd.concat([track_,track_pop],axis=0)
        except Exception as e:
            print(e)
            continue

    # Artist features
    for i in tqdm(range(0,len(artist_id_uni),25)):
        try:
            artist_features = sp.artists(artist_id_uni[i:i+25])
            for x in range(25):
                artist_df=pd.DataFrame([artist_id_uni[i+x]],columns=['artist_uri'])
                artist_pop = artist_features['artists'][x]["popularity"]
                artist_genres = artist_features['artists'][x]["genres"]
                artist_df["Artist_pop"] = artist_pop
                if artist_genres: 
                    artist_df["genres"] = " ".join([regex.sub(' ','_',i) for i in artist_genres])
                else:
                    artist_df["genres"] = "unknown"
                artist_=pd.concat([artist_,artist_df],axis=0)
        except Exception as e:
            print(e)
            continue

    # Combine dataframes into one test dataframe
    audio_features.drop(columns=['type','uri','track_href','analysis_url'],axis=1,inplace=True)
    test=pd.DataFrame(track_,columns=['track_uri','artist_uri','album_uri'])
    track_.drop(columns=(['artist_uri', 'album_uri']),inplace=True)
    test = pd.merge(test,audio_features, left_on = "track_uri", right_on= "id",how = 'inner')
    test = pd.merge(test,track_, left_on = "track_uri", right_on= "track_uri",how = 'inner')
    test = pd.merge(test,artist_, left_on = "artist_uri", right_on= "artist_uri",how = 'inner')
    test.rename(columns = {'Artist_pop':'artist_popularity','Track_pop': 'track_popularity', 'Track_release_date': 'release_date', 'Album_uri':'album_uri', 'Artist_genres': 'genres'},inplace=True)
    del audio_features,track_,artist_
    test.drop(columns=['id'],axis=1,inplace=True)
    test.dropna(axis=0,inplace=True)
    test['track_popularity'] = test['track_popularity'].apply(lambda x: int(x/5))
    test['artist_popularity'] = test['artist_popularity'].apply(lambda x: int(x/5))
    test['release_date'] = test['release_date'].apply(lambda x: x.split('-')[0])
    test['release_date']=test['release_date'].astype('int16')
    test['release_date'] = test['release_date'].apply(lambda x: int(x/50))
    test[['danceability', 'energy', 'key','loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness','liveness', 'valence', 'tempo', 'time_signature']]=test[['danceability', 'energy', 'key','loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness','liveness', 'valence', 'tempo','time_signature']].astype('float16')
    test[['duration_ms']]=test[['duration_ms']].astype('float32')
    test[['release_date', 'track_popularity', 'artist_popularity']]=test[['release_date', 'track_popularity', 'artist_popularity']].astype('int8')

    # Create the test and df dataframe
    df = df[['artist_name','artist_uri','artist_popularity',
         'album_name','album_uri',
         'track_name', 'track_uri','track_popularity',
         'danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo',
         'duration_ms','time_signature',
         'release_date','genres']]

    test = test[['artist_name','artist_uri','artist_popularity',
        'album_name','album_uri',
        'track_name', 'track_uri','track_popularity',
        'danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo',
        'duration_ms','time_signature',
        'release_date','genres']]

    df.drop_duplicates(subset=['track_uri'],inplace=True,keep='last') ## keep last to keep the dataset updated 
    df.dropna(axis=0,inplace=True)
    df = df[~df['track_uri'].isin(test['track_uri'].values)]

    # Work with separating genres
    test['genres'] = test['genres'].apply(lambda x: x.split(" "))
    tfidf = TfidfVectorizer() #max_features=5 
    tfidf_matrix = tfidf.fit_transform(test['genres'].apply(lambda x: " ".join(x)))
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['genre' + "|" + i for i in tfidf.get_feature_names_out()]
    genre_df=genre_df.astype('float16')
    test.drop(columns=['genres'],axis=1,inplace=True)
    test = pd.concat([test.reset_index(drop=True), genre_df.reset_index(drop=True)],axis = 1)
    test.isna().sum().sum()
    df['genres'] = df['genres'].apply(lambda x: x.split(" "))
    tfidf_matrix = tfidf.transform(df['genres'].apply(lambda x: " ".join(x)))
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['genre' + "|" + i for i in tfidf.get_feature_names_out()]
    genre_df=genre_df.astype('float16')
    df.drop(columns=['genres'],axis=1,inplace=True)
    df = pd.concat([df.reset_index(drop=True), genre_df.reset_index(drop=True)],axis = 1)

    try:
        df.drop(columns=['genre|unknown'],axis=1,inplace=True)
        test.drop(columns=['genre|unknown'],axis=1,inplace=True)
    except:
        print('genre|unknown not found')

    sc=MinMaxScaler()
    df.iloc[:,7:22] = sc.fit_transform(df.iloc[:,7:22])
    test.iloc[:,7:22]=sc.transform(test.iloc[:,7:22])
    playvec=pd.DataFrame(test.sum(axis=0)).T

    # Get the similarity matrix between the songs
    df['similarity']=cosine_similarity(df.drop(['track_name','track_uri','artist_name','artist_uri','album_name','album_uri'], axis = 1),playvec.drop(['track_name','track_uri','artist_name','artist_uri','album_name','album_uri'], axis = 1))
    df.sort_values(['similarity'],ascending = False,kind='stable',inplace=True)

    # Generate the final result dataframe
    Fresult = pd.DataFrame()
    for i in range(1000):
        result=pd.DataFrame([i])
        result['track_name'] = df.iloc[i].track_name
        result['artist_name'] = df.iloc[i].artist_name
        result['similarity'] = df.iloc[i].similarity
        result['album_uri'] = df.iloc[i].album_uri
        result['track_uri'] = df.iloc[i].track_uri
        Fresult=pd.concat([Fresult,result],axis=0)

    # Return the final dataframe
    Fresult['ranking'] = Fresult['similarity'].rank(method='dense', ascending=False)
    Fresult.sort_values(by=['ranking'], ascending=True)
    Fresult.to_csv("test_playlist.csv")

    """
    album_uri_ids = list(set(artist_id))
    # Track features
    for i in tqdm(range(0,len(track_ids_uni),25)):
        try:
            track_features = sp.tracks(track_ids_uni[i:i+25])
            for x in range(25):
                track_pop=pd.DataFrame([track_ids_uni[i+x]],columns=['track_uri'])
                track_pop['Track_release_date']=track_features['tracks'][x]['album']['release_date']
                track_pop['Track_pop'] = track_features['tracks'][x]["popularity"]
                track_pop['track_name']=track_features['tracks'][x]['name']
                track_pop['artist_uri']=track_features['tracks'][x]['artists'][0]['id']
                track_pop['album_uri']=track_features['tracks'][x]['album']['id']
                track_pop['album_name'] = track_features['tracks'][x]['album']['name']
                track_pop['artist_name'] = track_features['tracks'][x]['artists'][0]['name']
                track_=pd.concat([track_,track_pop],axis=0)
        except Exception as e:
            print(e)
            continue
    """

    return Fresult['track_name'].to_list(), Fresult['artist_name'].to_list(), Fresult['track_uri'].to_list()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)