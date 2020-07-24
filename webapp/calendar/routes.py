from flask import jsonify, render_template
from flask_login import current_user, login_required
from webapp.calendar import bp


@bp.route("/")
@login_required
def index():
    return render_template("calendar/index.html")


@bp.route("/data")
@login_required
def return_data():
    events = []
    # get all tasks of user
    tasks = current_user.get_tasks()
    for task in tasks:
        code = task.module.code.upper()
        title = task.title
        # create event
        event_title = f"{code}: {title}"
        event_start = task.start_timestamp
        event_end = task.end_timestamp
        event = {
            "title": event_title,
            "start": event_start,
            "end": event_end
        }
        # add event to list
        events.append(event)
    # return events list as json response
    return jsonify(events)
