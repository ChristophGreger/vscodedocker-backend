from flask import Blueprint


volumes = Blueprint('volumes', __name__, url_prefix="/volumes")

from app.volumes import routes, before

