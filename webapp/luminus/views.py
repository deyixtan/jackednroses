# webapp/luminus/views.py
import os
from flask import render_template, url_for
from flask_login import login_required, current_user
from webapp import db
from webapp.luminus import luminus
from webapp.models import Module, Enrolled, User
from wtforms import ValidationError


@luminus.route("/", defaults={"module_index": 0})
@luminus.route("/<int:module_index>")
@login_required
def index(module_index):
    #Gets the NUSNET ID of the current user
    user = User.query.filter_by(id=current_user.get_id()).first()
    enrolled = Enrolled.query.filter_by(user = user).all()
    module_list = []
    #Check if user has enrolled modules
    if enrolled:
        for mod in enrolled:
            module_list.append(Module.query.filter_by(id = mod.module_id).first())

        iframe = url_for('luminus.view_module', code=module_list[module_index].code)

        return render_template("luminus/index.html", module_list=module_list, iframe=iframe)
    else:
         return render_template("luminus/index.html")


@luminus.route("/view_module/<code>")
@login_required
def view_module(code):
    module = Module.query.filter_by(code=code).first_or_404()
    return render_template("luminus/view_module.html", code=module.code, name=module.name, academic_year=module.academic_year, semester=module.semester)
