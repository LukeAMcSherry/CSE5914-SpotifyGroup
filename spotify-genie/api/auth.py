from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/spotify')
def spotify():
    return {'number': 2}
