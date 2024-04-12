import json

from app.container import container
from app.database.models import Container


@container.route('/', methods=['GET'])
def index():
    liste = []
    for container_this in Container.getAll():
        list.append(container_this.to_dict())

    return json.dumps({"containers": liste})
