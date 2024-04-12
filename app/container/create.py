from app import db
from app.container import container
from flask import request
import app.jsonvalidation.container as jv
from app.database.models import Container, Image, Volume
import docker

client = docker.from_env()


@container.route('/create', methods=['PUT'])
def create():
    data = request.json

    try:
        jv.validate_create(data)
    except Exception as e:
        return "False request body: " + str(e), 402

    name = data["name"]
    description = data["description"]
    vorlagen_id = data["vorlagen_id"]
    connection_token = data["connection_token"]
    port = data["port"]
    volume_id = data["volume_id"]

    if len(connection_token.split(" ")) != 1:
        return "Connection token must not contain spaces", 402

    if db.session.execute(db.select(db.exists().where(Container.name == name))).scalar():
        return "Container already exists", 402

    image = db.session.execute(db.select(Image).where(Image.id == vorlagen_id)).scalars().first()

    if not image:
        return "Vorlage does not exist or has no image", 402

    volume = db.session.execute(db.select(Volume).where(Volume.id == volume_id)).scalars().first()

    if not volume:
        return "Volume does not exist", 402

    created_container = client.container.run(image.docker_id, name=name, detach=True, ports={f"3000/tcp": port}, command=f"--connection-token {connection_token}", volumes={volume.name: {"bind": "/home/workspace", "mode": "rw"}})

    container_this = Container(name=name, description=description, vorlagen_id=vorlagen_id, connection_token=connection_token, port=port, volume_id=volume_id)

    db.session.add(container_this)
    db.session.commit()
    return "Success", 200




