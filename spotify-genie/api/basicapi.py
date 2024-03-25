from flask import Flask, request, jsonify
from flask_cors import CORS
import auth
import home
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, 'Datasets')
app = Flask(__name__)
CORS(app)
app.secret_key = "dwasdwahdskajwdk"
app.register_blueprint(auth.auth_blueprint)
app.register_blueprint(home.home_blueprint)

# @app.route('/time')
# def get_current_time():
#     return {'time': time.time()}


GENIUS_ACCESS_TOKEN = "bFIwf618zPphfRGovJYks0NV0cBDbalfyKPUV1AI1Crv28_opQhjPuEIqq47SZBE"

def scrape_lyrics(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    lyrics_container = soup.find('div', {'data-lyrics-container': 'true'})
    
    if not lyrics_container:
        return 'Lyrics not found'

    # Remove script and other unnecessary tags
    for script in lyrics_container(["script", "style"]):
        script.decompose()

    lyrics = lyrics_container.get_text(' ', strip=True)
    # Replace sequences of spaces with a single newline
    lyrics = '\n'.join([line.strip() for line in lyrics.splitlines() if line])
    
    return lyrics


@app.route('/lyrics', methods=['POST'])
def lyrics():
    data = request.json
    song_title = data['title']
    artist_name = data['artist']
    headers = {'Authorization': f'Bearer {GENIUS_ACCESS_TOKEN}'}
    search_url = f"https://api.genius.com/search?q={artist_name}+{song_title}"

    try:
        genius_response = requests.get(search_url, headers=headers)
        genius_response.raise_for_status()  # Raises a HTTPError if the response status code is 4XX/5XX
        lyrics_data = genius_response.json()

        if 'response' in lyrics_data and 'hits' in lyrics_data['response'] and len(lyrics_data['response']['hits']) > 0:
            path = lyrics_data['response']['hits'][0]['result']['path']
            lyrics_url = f"https://genius.com{path}"
            lyrics = scrape_lyrics(lyrics_url)
            return jsonify({'lyrics': lyrics})
        else:
            return jsonify({'error': 'No lyrics found'}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
