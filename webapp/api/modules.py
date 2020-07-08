# webapp/api/modules.py
from webapp.api import api
from webapp.api.helpers import serialize_data, render_data
from webapp.models import Module, User


@api.route("/modules")
def fetch_modules():
    modules = Module.query.all()
    return render_data(serialize_data(modules))


@api.route("/modules/<int:module_id>")
def fetch_module(module_id):
    module = Module.query.get(module_id)
    return render_data(serialize_data(module))


@api.route("/modules/<int:module_id>/enrolled")
def fetch_users_enrolled(module_id):
    module = Module.query.get(module_id)

    # get enrolled users object
    enrolled_users = list()
    for entry in module.enrolled:
        user = User.query.filter_by(nusnetid=entry.nusnetid).first()
        enrolled_users.append(user)

    return render_data(serialize_data(enrolled_users))


@api.route("/modules/<int:module_id>/announcements")
def fetch_announcements(module_id):
    module = Module.query.get(module_id)

    # get annoucements object
    announcements = list()
    for entry in module.announcements:
        announcements.append(entry)

    return render_data(serialize_data(announcements))


@api.route("/modules/<int:module_id>/exams")
def fetch_exams(module_id):
    module = Module.query.get(module_id)

    # get exams object
    exams = list()
    for entry in module.exams:
        exams.append(entry)

    return render_data(serialize_data(exams))


@api.route("/modules/<int:module_id>/tasks")
def fetch_tasks(module_id):
    module = Module.query.get(module_id)

    # get tasks object
    tasks = list()
    for entry in module.tasks:
        tasks.append(entry)

    return render_data(serialize_data(tasks))
