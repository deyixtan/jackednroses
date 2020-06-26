# webapp/luminus/views.py
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from webapp import db
from webapp.luminus import luminus
from webapp.luminus.forms import CreateModuleForm, EnrolToModuleForm
from webapp.models import Module, Enrolled, User
from wtforms import ValidationError
import os

@luminus.route("/", defaults={"module_index": 0})
@luminus.route("/<int:module_index>")
@login_required
def index(module_index):
    #Gets the NUSNET ID of the current user
    user = User.query.filter_by(id=current_user.get_id()).first()
    enrolled = Enrolled.query.filter_by(user = user).all()
    module_list = []
    for mod in enrolled:
        module_list.append(Module.query.filter_by(id = mod.module_id).first())

    iframe = url_for('luminus.view_module', code=module_list[module_index].code)

    return render_template("luminus/index.html", module_list=module_list, iframe=iframe)

@luminus.route("/view_module/<code>/", defaults={"plugin_index": 0})
@luminus.route("/view_module/<code>/<int:plugin_index>")
@login_required
def view_module(code, plugin_index):
    module = Module.query.filter_by(code=code).first_or_404()

    print(f"module_id={module.id}, module_code={module.code}, module_ay={module.academic_year}, module_sem={module.semester}, plugin_index={plugin_index}")
    basedir = os.path.abspath(os.path.dirname(__name__))
    moduledir = os.path.join(basedir, "webapp", "luminus", "modules", module.code, module.academic_year.replace('/', ''), str(module.semester), "plugins")

    # plugins
    plugins = []
    for root, dirs, files in os.walk(moduledir):
        path = root.split(os.sep)
        package_name = os.path.basename(root)
        for file in files:
            if file == "info.json":
                import json
                with open(os.path.join(moduledir, package_name, file)) as f:
                    data = json.load(f)
                    plugins.append(data)

    print(plugins)

    return render_template("luminus/view_module.html", module=module, plugins=plugins, plugin_index=plugin_index)


@luminus.route("/register", methods=["GET", "POST"])
@login_required
def register():
    form = CreateModuleForm()
    if form.validate_on_submit():
        module = Module(code=form.code.data, name=form.name.data, academic_year=form.academic_year.data, semester=form.semester.data)
        db.session.add(module)
        db.session.commit()
        #create module directory if successfull
        basedir =  os.path.abspath(os.path.dirname(__name__)) #May be able to reference from config file
        module_path = os.path.join(basedir,'webapp', 'luminus', 'modules', form.code.data, form.academic_year.data.replace('/', ''), str(form.semester.data))
        if not os.path.exists(module_path):
            os.makedirs(module_path)
            
        flash("Successfully registered module.", "success")
        return redirect(url_for("core.index"))
    return render_template("luminus/register.html", form=form)

@luminus.route("/enrol_to_module", methods=["GET", "POST"])
@login_required
def enrol_to_module():
    form = EnrolToModuleForm()
    if form.validate_on_submit():
        enrolled = Enrolled(nusnetid = form.nusnetid.data, code = form.code.data, academic_year = form.academic_year.data, semester = form.semester.data)
        db.session.add(enrolled)
        db.session.commit()
        flash("Successfully enrolled student to module.", "success")
        #return redirect(url_for(luminus.enrol_to_module))
        return redirect(url_for("core.index"))
    return render_template("luminus/enrol_to_module.html", form=form)