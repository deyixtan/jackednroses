from flask import render_template
from flask_login import current_user, login_required
from webapp.luminus import bp


@bp.route("/", defaults={"index": 0})
@bp.route("/<int:index>/")
@login_required
def view_module(index):
    # get current viewed module
    modules = current_user.get_current_modules()
    module = modules[index]
    # get module enabled plugins
    plugins = module.plugins.all()

    return render_template("luminus/index.html", module=module, plugins=plugins)
