from flask import Blueprint

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route("/")
def home():
    pass
