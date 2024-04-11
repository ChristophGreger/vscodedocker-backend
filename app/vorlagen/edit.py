import threading

from app.database.models import Vorlage, Container, Image
from app.vorlagen import vorlagen
from app import db
import app.mydocker.main as mydocker
import json
from flask import request
from sqlalchemy.sql import text


@vorlagen.route("/edit", methods=["PATCH"])
def edit_vorlage():
    data = request.json

    try:
        name = data["name"]
        description = data["description"]
        vscodeextension = data["vscodeextension"]
        installcommands = data["installcommands"]
        version = data["version"]

        if not isinstance(version, int):
            raise Exception("version must be an int")

        if not name or not description or not vscodeextension or not installcommands:
            raise Exception("Missing required fields")

        if not isinstance(vscodeextension, list):
            raise Exception("vscodeextension must be a list")
        if not isinstance(installcommands, list):
            raise Exception("installcommands must be a list")
    except Exception as e:
        return "False request body because of " + str(e), 402

    if not db.session.execute(db.select(db.exists().where(Vorlage.name == name))).scalar():
        return "Vorlage does not exist", 403

    previousvorlage = db.session.execute(db.select(Vorlage).where(Vorlage.name == name)).order_by(
        text("version desc")).first().scalar()
    if previousvorlage.id >= version:
        return "Version must be greater than the previous version", 402

    vorlage = Vorlage(name=name, description=description, vscodeextension=json.dumps(vscodeextension),
                      installcommands=json.dumps(installcommands), version=version)

    db.session.add(vorlage)
    db.session.commit()

    vorlage = db.session.execute(db.select(Vorlage).where(Vorlage.name == name, Vorlage.version == version)).scalar()

    threading.Thread(target=mydocker.make_image,
                     args=(vorlage.id, name, vorlage.version, json.dumps(vscodeextension), json.dumps(installcommands))).start()

    return "Success", 200


@vorlagen.route("/edit", methods=["DELETE"])
def delete_vorlage():
    # parameter validation
    name = request.args.get("name")
    version = request.args.get("version")
    _id = request.args.get("id")

    vorlage = None

    if _id:
        vorlage = db.session.execute(db.select(Vorlage).where(Vorlage.id == _id)).scalar()
        if not vorlage:
            return "Vorlage does not exist", 404
    elif name and version:
        vorlage = db.session.execute(db.select(Vorlage).where(Vorlage.name == name, Vorlage.version == version)).scalar()
        if not vorlage:
            return "Vorlage does not exist", 404
    if vorlage:
        _id = vorlage.id
        if db.session.execute(db.select(Container).where(Container.id_vorlage == _id)).scalar():
            return "Vorlage is in use", 405
        db.session.delete(vorlage)
        image = db.session.execute(db.select(Image).where(Image.id_vorlage == _id)).scalar()
        if image:
            image.delete_file()
        db.session.delete(image)
        db.session.commit()
        return "Success", 200

    if not name:
        return "Missing name", 402
    alle_vorlagen = db.session.execute(db.select(Vorlage).where(Vorlage.name == name)).scalars().all()
    if not alle_vorlagen:
        return "Vorlage does not exist", 404

    for x in alle_vorlagen:
        if db.session.execute(db.select(Container).where(Container.id_vorlage == x.id)).scalar():
            return "Vorlage is still in use", 405
    for x in alle_vorlagen:
        image = db.session.execute(db.select(Image).where(Image.id_vorlage == x.id)).scalar()
        if image:
            image.delete_file()
        db.session.delete(image)
    db.session.delete(alle_vorlagen)
    db.session.delete(db.session.execute(db.select(Image).where(Image.id_vorlage == _id)).scalars())
    db.session.commit()
    return "Success", 200
