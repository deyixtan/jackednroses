# webapp/api/exams.py
from webapp.api import api
from webapp.api.helpers import serialize_data, render_data
from webapp.models import Exam


@api.route("/exams")
def fetch_exams():
    exams = Exam.query.all()
    return render_data(serialize_data(exams))


@api.route("/exams/<int:exam_id>")
def fetch_exam(exam_id):
    exam = Exam.query.get(exam_id)
    return render_data(serialize_data(exam))


@api.route("/exams/<int:exam_id>/examdetails")
def fetch_exam_users(module_id):
    exam = Module.query.get(exam_id)

    # get users object
    users = list()
    for entry in exam.examdetails:
        user = User.query.filter_by(nusnetid=entry.nusnetid).first()
        users.append(user)

    return render_data(serialize_data(users))
