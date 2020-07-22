from datetime import datetime
from flask import render_template, request
from flask_login import current_user, login_required
from webapp.core import bp
from webapp.models import ModuleAnnouncement, ModuleTask, Module, User, Plugin, UHMSMessage


@bp.route("/")
@login_required
def index():
    modules = current_user.get_current_modules()
    announcements = []
    for module in modules:
        announcements.extend(module.get_announcements())
    tasks = current_user.get_current_tasks()
    return render_template("index.html", title="Homepage", announcements=announcements, tasks=tasks)


@bp.route("/account")
@login_required
def account():
    return render_template("account.html")
