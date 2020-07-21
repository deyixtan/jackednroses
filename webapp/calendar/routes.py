import json
from flask import render_template, request
from flask_login import current_user, login_required
from webapp.calendar import bp
from webapp.models import ModuleAnnouncement, ModuleTask, Module, User, Plugin, UHMSMessage


@bp.route("/")
@login_required
def index():
    return render_template("calendar_index.html")


# helper function
def create_event(title, timestamp):
    return {
        "title": title,
        "start": timestamp.strftime("%Y-%m-%d")
    }


@bp.route("/data")
@login_required
def return_data():
    events = []
    tasks = current_user.tasks.all()
    for task in tasks:
        code = task.module.code
        title = task.title
        timestamp = task.timestamp
        event = create_event(f"{code}: {title}", timestamp)
        events.append(event)
    return json.dumps(events)
