from flask_login import login_required, current_user
from flask import render_template, url_for
from webapp.uhms import bp
from webapp.models import UhmsMessages


@bp.route("/")
@login_required
def index():
    message_list = UhmsMessages.query.all()

    return render_template("uhms/index.html", message_list=message_list, user=current_user)
