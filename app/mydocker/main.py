import docker
from io import StringIO
import json
from app.database.models import Image
from app import db

client = docker.from_env()


def make_image(vorlagen_id, name, version, vscodeextension, installcommands):

    with open("/app/mydocker/_dockerfile", "r") as file:
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
        commands += "    " + command + "&& \\"

    commands = commands[:-4]

    dockerfile = dockerfile.replace("{toreplaceforcommands}", commands)

    dockerstringio = StringIO(dockerfile)

    image, logs = client.images.build(fileobj=dockerstringio, tag=f"{name}:{version}")

    from app import app

    with app.app_context():
        image = Image(name=f"{name}:{version}", version=version, id_vorlage=vorlagen_id)
        db.session.add(image)
        db.session.commit()





