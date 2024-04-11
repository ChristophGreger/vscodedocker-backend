from app.auth.login import login_required
from app.volumes import volumes


@volumes.before_request
@login_required
def before_request():
    pass
