import os
from flask import render_template, url_for
from flask_login import current_user, login_required
from wtforms import ValidationError
from webapp import db
from webapp.luminus import bp
from webapp.models import ModuleAnnouncement, ModuleTask, Module, User, Plugin, UHMSMessage


@bp.route("/", defaults={"module_index": 0})
@bp.route("/<int:module_index>")
@login_required
def index(module_index):
    modules = current_user.get_current_modules()
    if len(modules) > 0:
        iframe = url_for('luminus.view_module', code=modules[module_index].code)
        return render_template("luminus/index.html", title="LumiNUS", modules=modules, iframe=iframe)
    else:
        return render_template("luminus/index.html", title="LumiNUS")


@bp.route("/view_module/<code>/", defaults={"plugin_index": 0})
@bp.route("/view_module/<code>/<int:plugin_index>")
@login_required
def view_module(code, plugin_index):
    module = Module.query.filter_by(code=code).first_or_404()
    basedir = os.path.abspath(os.path.dirname(__name__))
    moduledir = os.path.join(basedir, "webapp", "luminus", "modules", module.code, str(module.academic_year), str(module.semester), "plugins")

    # plugins
    plugins = []
    for root, dirs, files in os.walk(moduledir):
        package_name = os.path.basename(root)
        # print(f"I'm in {package_name}, files i have=<{files}>, dirs i have=<{dirs}>")
        for file in files:
            if file == "info.json":
                import json
                with open(os.path.join(moduledir, package_name, file)) as f:
                    data = json.load(f)
                    plugins.append(data)

    return render_template("luminus/view_module.html", module=module, plugins=plugins, plugin_index=plugin_index)


# LUMINUS ROUTES

# PLUGIN ROUTES

@bp.route("/modules/<code>/announcements/")
@login_required
def module_announcements(code):
    module = Module.query.filter_by(code=code).first_or_404()
    announcements = module.announcements.all()
    return render_template("plugins/announcements/index.html", announcements=announcements)
