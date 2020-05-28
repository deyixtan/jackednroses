# webapp/core/views.py
from flask import render_template, request, Blueprint
from flask_login import login_required

core = Blueprint("core", __name__)

@core.route("/")
@login_required
def index():
    return render_template("index.html")

@core.route("/account")
@login_required
def account():
    return render_template("account.html")
