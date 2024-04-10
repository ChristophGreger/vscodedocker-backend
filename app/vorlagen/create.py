from app.database.models import Vorlage
from app.vorlagen import vorlagen
from app import db
import app.mydocker.main as mydocker
from flask import request
import json
import threading


@vorlagen.route('/create', methods=["PUT"])
def create():
    data = request.json
    try:
        name = data["name"]
        description = data["description"]
        vscodeextension = data["vscodeextension"]
        installcommands = data["installcommands"]

        if not name or not description or not vscodeextension or not installcommands:
            raise Exception("Missing required fields")

        if not isinstance(vscodeextension, list):
            raise Exception("vscodeextension must be a list")
        if not isinstance(installcommands, list):
            raise Exception("installcommands must be a list")

    except:
        return "False request body", 402

    if db.session.execute(db.select(db.exists().where(Vorlage.name == name))).scalar():
        return "Vorlage already exists", 402

    vorlage = Vorlage(name=name, description=description, vscodeextension=json.dumps(vscodeextension),
                      installcommands=json.dumps(installcommands), version=100)
    db.session.add(vorlage)
    db.session.commit()

    vorlagen_id = db.session.scalar(db.select(Vorlage.id).where(Vorlage.name == name))

    # Start thread to create the image
    threading.Thread(target=mydocker.make_image, args=(vorlagen_id, name, 100, json.dumps(vscodeextension), json.dumps(installcommands))).start()

    return "Success", 200