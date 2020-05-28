# webapp/luminus/views.py
from flask import Blueprint
from flask_login import login_required

luminus = Blueprint("luminus", __name__)

@luminus.route("/")
@login_required
def index():
    return "Hello LumiNUS"
