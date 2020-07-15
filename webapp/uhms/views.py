from flask_login import login_required
from webapp.uhms import bp


@bp.route("/")
@login_required
def index():
    return "Hello UHMS"
