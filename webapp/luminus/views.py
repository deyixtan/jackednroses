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


@luminus.route("/view_module/<code>/", defaults={"plugin_index": 0})
@luminus.route("/view_module/<code>/<int:plugin_index>")
@login_required
def view_module(code, plugin_index):
    module = Module.query.filter_by(code=code).first_or_404()
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

