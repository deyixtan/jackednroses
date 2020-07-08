# webapp/api/users.py
from webapp.api import api
from webapp.api.helpers import serialize_data, render_data
from webapp.models import Exam, Module, User


@api.route("/users")
def fetch_users():
    users = User.query.all()
    return render_data(serialize_data(users))


@api.route("/users/<int:user_id>")
def fetch_user(user_id):
    user = User.query.get(user_id)
    return render_data(serialize_data(user))


@api.route("/users/<int:user_id>/enrolled")
def fetch_modules_enrolled(user_id):
    user = User.query.get(user_id)

    # get enrolled modules object
    enrolled_modules = list()
    for entry in user.enrolled:
        module = Module.query.get(entry.module_id)
        enrolled_modules.append(module)

    return render_data(serialize_data(enrolled_modules))


@api.route("/users/<int:user_id>/userdetails")
def fetch_user_details(user_id):
    user = User.query.get(user_id)

    details = list()
    for entry in user.userdetails:
        details.append(entry)

    return render_data(serialize_data(details))


@api.route("/users/<int:user_id>/examdetails")
def fetch_user_exams(user_id):
    user = User.query.get(user_id)

    # get exams object + seatnum
    exams = list()
    for entry in user.examdetails:
        exam = Exam.query.get(entry.exam_id)
        exams.append({
            "seatnum": entry.seatnum,
            "exam": exam
        })

    # serialize data
    for index, entry in enumerate(exams):
        exams[index]["exam"] = serialize_data(entry["exam"])

    return render_data(exams)
