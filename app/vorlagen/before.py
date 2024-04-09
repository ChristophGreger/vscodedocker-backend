from app.vorlagen import vorlagen
from app.auth.login import login_required


@vorlagen.before_request
@login_required
def before_request():
    pass
