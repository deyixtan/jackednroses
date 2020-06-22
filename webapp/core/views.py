# webapp/core/views.py
from flask import render_template, request
from flask_login import current_user, login_required
from webapp.core import core
from webapp.models import Enrolled, Module, User, Announcement

@core.route("/")
@login_required
def index():
    #Gets the NUSNET ID of the current user
    user = User.query.filter_by(id=current_user.get_id()).first()
    enrolled = Enrolled.query.filter_by(user = user).all()
    
    announcement_list= []
    for enrol_entry in enrolled:
        mod = Module.query.get(enrol_entry.module_id)
        announcement_list.extend(mod.announcements)
    #print(announcement_list)
    announcement_list = sorted(announcement_list, key=lambda x: x.date, reverse=True)
    return render_template("index.html", announcement_list = announcement_list)

@core.route("/account")
@login_required
def account():
    return render_template("account.html", user=current_user)
