from flask import Blueprint

images = Blueprint("images", __name__, url_prefix="/images")

from app.images import routes, before