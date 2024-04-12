import json

from . import images
from ..database.models import Image
from flask import request


@images.route("/", methods=["GET"])
def list_images():
    returning_images = []
    for image in Image.get_All():
        returning_images.append(image.to_dict())

    return {"images": returning_images}


@images.route("/", methods=["DELETE"])
def delete():
    _id = request.args.get("id")
    name = request.args.get("name")

    image = None

    if _id:
        image = Image.by_id(_id)

    if not _id:
        image = Image.by_name(name)

    if not image:
        return "No Image with that id/name", 404

    boolean, message = image.delete()

    if not boolean:
        return json.dumps(image.to_dict()), 405

    return "Success", 200
