import docker
from io import StringIO
import json

client = docker.from_env()


def make_image(name, version, vscodeextension, installcommands):

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

    client.images.build(fileobj=dockerstringio, tag=f"{name}:{version}")

    # TODO register the image in the database





