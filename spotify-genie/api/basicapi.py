import time
from flask import Flask
import auth

app = Flask(__name__)
app.register_blueprint(auth.auth)


@app.route('/time')
def get_current_time():
    return {'time': time.time()}
