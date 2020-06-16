# webapp/core/views.py
from flask import render_template, request
from flask_login import current_user, login_required
from webapp.core import core

@core.route("/")
@login_required
def index():
    return render_template("index.html")

@core.route("/account")
@login_required
def account():
    return render_template("account.html", user=current_user)
