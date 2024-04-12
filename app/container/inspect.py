import json

from app import db
from app.container import container
from flask import request

from app.database.models import Container


@container.route('/inspect', methods=['GET'])
def inspect():
    _id = request.args.get('id')
    name = request.args.get("name")

    container_this = None

    if _id is None and name is None:
        return "No id or name given", 404

    if _id is not None:
        container_this = db.session.execute(db.select(Container).where(Container.id == _id)).scalar().first()
    else:
        container_this = db.session.execute(db.select(Container).where(Container.name == name)).scalar().first()

    if container_this is None:
        return "Container not found", 403

    return json.dumps(container_this.to_dict()), 200
