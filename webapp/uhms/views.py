# webapp/uhms/views.py
from flask import Blueprint
from flask_login import login_required

uhms = Blueprint("uhms", __name__)

@uhms.route("/")
@login_required
def index():
    return "Hello UHMS"
