from app.container import container


@container.route('/action', methods=['POST'])
def action():
    pass


@container.route('/action', methods=['DELETE'])
def delete():
    pass
