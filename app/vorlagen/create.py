from app.database.models import Vorlage
from app.vorlagen import vorlagen
from app import db
import app.mydocker.main as mydocker
from flask import request
import json
import app.jsonvalidation.vorlagen as jv


@vorlagen.route('/create', methods=["PUT"])
def create():
    data = request.json

    try:
        jv.validate_create(data)
    except Exception as e:
        return "False request body: " + str(e), 402

    name = data["name"]
    description = data["description"]
    vscodeextension = data["vscodeextension"]
    installcommands = data["installcommands"]

    if db.session.execute(db.select(db.exists().where(Vorlage.name == name))).scalar():
        return "Vorlage already exists", 402

    vorlage = Vorlage(name=name, description=description, vscodeextension=json.dumps(vscodeextension),
                      installcommands=json.dumps(installcommands), version=100)

    db.session.add(vorlage)
    db.session.commit()

    vorlagen_id = db.session.scalar(db.select(Vorlage.id).where(Vorlage.name == name))

    # Start thread to create the image
    mydocker.make_image_thread(vorlagen_id, name, 100, json.dumps(vscodeextension), json.dumps(installcommands))

    return "Success", 200
