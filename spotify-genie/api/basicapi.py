from flask import Flask, request
from flask_cors import CORS
import auth
import home

app = Flask(__name__)
CORS(app)
app.secret_key = "dwasdwahdskajwdk"
app.register_blueprint(auth.auth_blueprint)
app.register_blueprint(home.home_blueprint)

# @app.route('/time')
# def get_current_time():
#     return {'time': time.time()}

@app.route('/process_playlist', methods=['POST'])
def process_playlist():

    print("retsp")
    try:
        playlist_uri = request.json['playlist_uri']
        # Log the received playlist URI
        print("Received playlist URI:", playlist_uri)
        # Process the playlist URI here
        # You can call your Python function with the playlist URI
        # Example:
        # result = my_python_function(playlist_uri)
        
        # Return a response indicating success
        return {'success': True, 'message': playlist_uri}
    except Exception as e:
        # Log any errors
        print("Error:", e)
        # Return a response indicating failure
        return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)