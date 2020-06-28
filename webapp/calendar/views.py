# webapp/calendar/views.py
import json
from flask import render_template, request
from flask_login import current_user, login_required
from webapp.calendar import calendar
from webapp.models import Enrolled, Module, User, Announcement, Task, Exam

@calendar.route("/")
@login_required
def index():
    return render_template("calendar_index.html")

# helper function
def create_event(title, timestamp):
    return {
        "title": title,
        "start": timestamp.strftime("%Y-%m-%d")
    }

@calendar.route("/data")
@login_required
def return_data():
    user = User.query.filter_by(id=current_user.get_id()).first()
    enrolled = Enrolled.query.filter_by(user = user).all()
    task_exam_list = []
    events_list = []
    for enrol_entry in enrolled:
        mod = Module.query.get(enrol_entry.module_id)
        task_exam_list.extend(mod.tasks)
        task_exam_list.extend(mod.exams)

    for task_exam in task_exam_list:
        if isinstance(task_exam, Task):
            events_list.append(create_event(task_exam.taskname, task_exam.timestamp))
        elif isinstance(task_exam, Exam):
            events_list.append(create_event(task_exam.examname, task_exam.timestamp))
    
    return json.dumps(events_list)