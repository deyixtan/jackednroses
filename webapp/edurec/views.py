# webapp/edurec/views.py
from flask import Blueprint
from flask_login import login_required

edurec = Blueprint("edurec", __name__)

@edurec.route("/")
@login_required
def index():
    return "Hello EduREC"
