import time
from flask import Flask
import auth
import home

app = Flask(__name__)
app.register_blueprint(auth.auth_blueprint)
app.register_blueprint(home.home_blueprint)

# @app.route('/time')
# def get_current_time():
#     return {'time': time.time()}
