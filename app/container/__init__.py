from flask import Blueprint

container = Blueprint('container', __name__, url_prefix="/container")

from app.container import create, action, inspect, index, before
