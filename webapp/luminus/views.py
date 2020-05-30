# webapp/luminus/views.py
from flask import flash, redirect, render_template, url_for, Blueprint
from flask_login import login_required
from webapp import db
from webapp.luminus.forms import CreateModuleForm
from webapp.models import Module

luminus = Blueprint("luminus", __name__)

@luminus.route("/")
@login_required
def index():
    modules = Module.query.all()
    return render_template("luminus/index.html", modules=modules)

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
        return redirect(url_for("luminus.index"))

    return render_template("luminus/register.html", form=form)
