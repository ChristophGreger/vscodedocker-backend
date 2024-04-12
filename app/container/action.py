from app import db
from app.container import container
from flask import request
from app.database.models import Container
import docker

client = docker.from_env()


@container.route('/action', methods=['POST'])
def action():
    name = request.args.get("name")
    _id = request.args.get("id")
    _action = request.args.get("action")

    if name is None and _id is None:
        return "No id or name given", 404

    if _action is None:
        return "No action given", 404

    container_this = None

    if _id is not None:
        container_this = db.session.execute(db.select(Container).where(Container.id == _id)).scalar().first()
    else:
        container_this = db.session.execute(db.select(Container).where(Container.name == name)).scalar().first()

    if container_this is None:
        return "Container not found", 404

    docker_container = client.containers.get(container_this.name)

    if not docker_container:
        return "Container not found", 404

    if _action == "start":
        try:
            docker_container.start()
        except Exception as e:
            return str(e), 402
    elif _action == "stop":
        try:
            docker_container.stop()
        except Exception as e:
            return str(e), 402
    elif _action == "restart":
        try:
            docker_container.restart()
        except Exception as e:
            return str(e), 402
    else:
        return "Unknown action", 404

    return "Success", 200


@container.route('/action', methods=['DELETE'])
def delete():
    name = request.args.get("name")
    _id = request.args.get("id")
    forcedelete = request.args.get("forcedelete")

    if name is None and _id is None:
        return "No id or name given", 404

    if forcedelete is None:
        forcedelete = False

    if forcedelete == "True":
        forcedelete = True
    elif forcedelete == "False":
        forcedelete = False

    container_this = None

    if _id is not None:
        container_this = db.session.execute(db.select(Container).where(Container.id == _id)).scalar().first()
    else:
        container_this = db.session.execute(db.select(Container).where(Container.name == name)).scalar().first()

    if container_this is None:
        return "Container not found", 404

    docker_container = client.containers.get(container_this.name)

    if not docker_container:
        return "Container not found", 404

    try:
        docker_container.remove(force=forcedelete)
    except Exception as e:
        return str(e), 402

    container_this.delete()

    return "Success", 200
