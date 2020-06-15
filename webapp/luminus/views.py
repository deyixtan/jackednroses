# webapp/luminus/views.py
from flask import flash, redirect, render_template, url_for, Blueprint
from flask_login import login_required, current_user
from webapp import db
from webapp.luminus.forms import CreateModuleForm, EnrollToModuleForm
from webapp.models import Module, Enrolled, User
from wtforms import ValidationError

luminus = Blueprint("luminus", __name__)

@luminus.route("/")
@login_required
def index():
    #Gets the NUSNET ID of the current user
    user = User.query.filter_by(id=current_user.get_id()).first()
    enrolled = Enrolled.query.filter_by(user = user).all()
    module_list = []
    for mod in enrolled:
        module_list.append(Module.query.filter_by(id = mod.module_id).first())
    return render_template("luminus/index.html", module_list=module_list)

@luminus.route("/view_module/<code>")
@login_required
def view_module(code):
    module = Module.query.filter_by(code=code).first_or_404()
    return render_template("luminus/view_module.html", code=module.code, name=module.name, academic_year=module.academic_year, semester=module.semester)

@luminus.route("/register", methods=["GET", "POST"])
@login_required
def register():
    form = CreateModuleForm()
    if form.validate_on_submit():
        module = Module(code=form.code.data, name=form.name.data, academic_year=form.academic_year.data, semester=form.semester.data)
        db.session.add(module)
        db.session.commit()
        flash("Successfully registered module.", "success")
        return redirect(url_for("core.index"))
        #return redirect(url_for("luminus.index"))
    return render_template("luminus/register.html", form=form)

@luminus.route("/enroll_to_module", methods=["GET", "POST"])
@login_required
def enroll_to_module():
    form = EnrollToModuleForm()
    if form.validate_on_submit():
        enrolled = Enrolled(nusnetid = form.nusnetid.data, code = form.code.data, academic_year = form.academic_year.data, semester = form.semester.data)
        db.session.add(enrolled)
        db.session.commit()
        flash("Successfully enrolled student to module.", "success")
        #return redirect(url_for(luminus.enroll_to_module))
        return redirect(url_for("core.index"))
    return render_template("luminus/enroll_to_module.html", form=form)