from app.database.models import Vorlage
from app.vorlagen import vorlagen
from flask import request
import json


@vorlagen.route('/inspect', methods=['GET'])
def inspect():
    vorlage = None
    _id = request.args.get("id")
    name = request.args.get("name")
    version = request.args.get("version")

    vorlage = Vorlage.get(name, _id, version)

    if not vorlage:
        return "Vorlage not found", 404

    returning = vorlage.toJson()

    return json.dumps(returning), 200
