from app.container import container
from app.auth.login import login_required


@container.before_request
@login_required
def before_request():
    pass
