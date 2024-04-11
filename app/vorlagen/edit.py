import threading

from app.database.models import Vorlage, Container, Image
from app.vorlagen import vorlagen
from app import db
import app.mydocker.main as mydocker
import json
from flask import request
from sqlalchemy.sql import text
import app.jsonvalidation.vorlagen as jv


@vorlagen.route("/edit", methods=["PATCH"])
def edit_vorlage():
    data = request.json

    try:
        jv.validate_edit(data)
    except Exception as e:
        return "False request body because of: " + str(e), 402

    name = data["name"]
    description = data["description"]
    vscodeextension = data["vscodeextension"]
    installcommands = data["installcommands"]
    version = data["version"]

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

    if not _id and not version and name:
        for x in db.session.execute(db.select(Vorlage).where(Vorlage.name == name)).scalars().all():
            x.delete()

    vorlage = Vorlage.get(name, _id, version)

    if not vorlage:
        return "Vorlage does not exist", 404

    vorlage.delete()

    return "Success", 200
