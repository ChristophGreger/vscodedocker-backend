from . import images


@images.route("/", methods=["GET"])
def list_images():
    pass


@images.route("/", methods=["DELETE"])
def delete():
    pass
