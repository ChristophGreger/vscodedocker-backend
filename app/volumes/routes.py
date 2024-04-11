import json
from flask import request
from app.database.models import Volume
from app.volumes import volumes
import app.mydocker.main as mydocker
from app import db


@volumes.route("/", methods=["GET"])
def list_volumes():
    returning = {}
    volumes_list = []
    for volume in Volume.getAll():
        volume_dict = {
            "id": volume.id,
            "name": volume.name,
            "usedin": [container.id for container in volume.get_usedin()]
        }
        volumes_list.append(volume_dict)

    returning["volumes"] = volumes_list
    returning = json.dumps(returning)


@volumes.route("/", methods=["PUT"])
def create_volume():
    name = request.args["name"]
    trying = mydocker.create_volume(name)
    if not trying:
        return "Volume already exists, or no name provided", 405
    return "Volume created", 200


@volumes.route("/", methods=["DELETE"])
def delete_volume():
    _id = request.args["id"]
    if _id:
        volume = db.session.execute(db.select(Volume).where(Volume.id == _id)).scalars().first()
        if not volume:
            return "Volume not found", 404
        trying = mydocker.delete_volume(volume.name)
        if not trying:
            return "Volume not found", 404
        return "Volume deleted", 200
    name = request.args["name"]
    trying = mydocker.delete_volume(name)
    if not trying:
        return "Volume not found", 404
    return "Volume deleted", 200

