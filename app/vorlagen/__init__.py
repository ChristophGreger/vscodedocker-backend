from flask import Blueprint

vorlagen = Blueprint('vorlagen', __name__, url_prefix="/vorlagen")

from app.vorlagen import create, edit, inspect, index, before
