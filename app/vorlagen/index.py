from app.database.models import Vorlage
from app.vorlagen import vorlagen
from app import db
import json


@vorlagen.route('/', methods=['GET'])
def index():
    allevorlagen = db.session.scalars(db.select(Vorlage))
    liste = []
    for x in allevorlagen:
        liste.append(x.name)
    returning = {"names": liste}
    return json.dumps(returning)
