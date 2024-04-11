from app import db
from app.database.models import Vorlage, Image, Container
from app.vorlagen import vorlagen
from flask import request
from sqlalchemy.sql import text
import json


@vorlagen.route('/inspect', methods=['GET'])
def inspect():
    vorlage = None
    if request.args.get("id"):
        _id = request.args.get("id")
        vorlage = db.session.scalar(db.select(Vorlage).where(Vorlage.id == _id))
    elif request.args.get("name"):
        name = request.args.get("name")
        if request.args.get("version"):
            # Get the specific version
            version = request.args.get("version")
            vorlage = db.session.scalar(db.select(Vorlage).where(Vorlage.name == name, Vorlage.version == version))
        else:
            # Get the latest version if no version is specified
            vorlage = db.session.scalar(
                db.select(Vorlage).where(Vorlage.name == name).order_by(text("version desc")).limit(1))

    if not vorlage:
        return "Vorlage not found", 404

    returning = {}
    returning["id"] = vorlage.id
    returning["name"] = vorlage.name
    returning["version"] = vorlage.version
    returning["description"] = vorlage.description
    returning["vscodeextension"] = json.loads(vorlage.vscodeextension)
    returning["installcommands"] = json.loads(vorlage.installcommands)

    usedin = []


# TODO: Not tested yet
    for image in db.session.scalars(db.select(Image).where(Image.id_vorlage == vorlage.id)):
        for container in db.session.scalars(db.select(Container).where(Container.id_image == image.id)):
            usedin.append(container.id)

    returning["usedin"] = usedin

    returning["image_id"] = db.session.scalar(db.select(Image.id).where(Image.id_vorlage == vorlage.id))

    existingversions = []

    for vorlage in db.session.scalars(db.select(Vorlage).where(Vorlage.name == name)):
        existingversions.append(vorlage.version)

    returning["existingversions"] = existingversions

    return json.dumps(returning), 200
