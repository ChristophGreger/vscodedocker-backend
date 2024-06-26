import docker
from io import BytesIO
import json
from app.database.models import Image, Volume
from app import db
import threading

client = docker.from_env()


def make_image(vorlagen_id, name, version, vscodeextension, installcommands):
    global logs
    logs = []
    name = name.lower()

    with open("./app/mydocker/_dockerfile", "r") as file:
        dockerfile = file.read()

    extensionsstring = vscodeextension
    extensionsstring = json.loads(extensionsstring)
    extensions = ""

    for extension in extensionsstring:
        extensions += "        " + extension + "\\ \n"

    dockerfile = dockerfile.replace("{toreplaceforaddons}", extensions)

    commandsstring = installcommands
    commandsstring = json.loads(commandsstring)
    commands = ""

    for command in commandsstring:
        commands += "    " + command + " && "

    commands = commands[:-4]

    dockerfile = dockerfile.replace("{toreplaceforcommands}", commands)

    dockerstringio = BytesIO(bytes(dockerfile, "ascii"))

    print("Building image")

    docker_id = None

    try:
        image, logs = client.images.build(fileobj=dockerstringio, forcerm=True, rm=True)
        docker_id = image.id
    except Exception as e:
        print(e)

    print("Image built")

    # for x in logs:
    #     print(x)

    from app import app

    with app.app_context():
        image = Image(name=f"{name}:{version}", version=version, id_vorlage=vorlagen_id, docker_id=docker_id)
        db.session.add(image)
        db.session.commit()


def make_image_thread(*args):
    threading.Thread(target=make_image,
                     args=args).start()


def create_volume(name):
    if not name:
        return False
    if client.volumes.list(filters={"name": name}):
        return False
    client.volumes.create(name=name)
    volume = Volume(name=name)
    db.session.add(volume)
    db.session.commit()
    return True


def delete_volume(name):
    if not name:
        return False
    if not client.volumes.list(filters={"name": name}):
        return False
    client.volumes.get(name).remove()
    volume = db.session.execute(db.select(Volume).where(Volume.name == name)).scalars().first()
    db.session.delete(volume)
    db.session.commit()
    return True



