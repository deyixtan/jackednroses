from flask import render_template
from flask_login import current_user, login_required
from webapp.core import bp


@bp.route("/")
@login_required
def index():
    # get announcements
    modules = current_user.get_current_modules()
    announcements = []
    for module in modules:
        announcements.extend(module.get_announcements())
    # get all current tasks
    tasks = current_user.get_current_tasks()
    return render_template("core/index.html", announcements=announcements, tasks=tasks)
