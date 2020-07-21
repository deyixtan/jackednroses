from flask_login import login_required, current_user
from flask import render_template, url_for
from webapp.uhms import bp
from webapp.models import ModuleAnnouncement, ModuleTask, Module, User, Plugin, UHMSMessage


@bp.route("/")
@login_required
def index():
    message_list = UHMSMessage.query.all()

    return render_template("uhms/index.html", message_list=message_list, user=current_user)
