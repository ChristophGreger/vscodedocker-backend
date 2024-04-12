from app.images import images
from app.auth.login import login_required


@images.before_request
@login_required
def before_request():
    pass
