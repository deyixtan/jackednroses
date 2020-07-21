import os
from flask import render_template, url_for, send_file, abort
from flask_login import current_user, login_required
from webapp.luminus import bp
from webapp.models import Module


@bp.route("/", defaults={"module_index": 0})
@bp.route("/<int:module_index>/")
@login_required
def index(module_index):
    modules = current_user.get_current_modules()
    current_module = modules[module_index]
    title = f"LumiNUS - {current_module.code.upper()}"

    if len(modules) > 0:
        plugins = modules[module_index].plugins.all()
        if len(plugins) > 0:
            module_id = modules[module_index].id
            return render_template("luminus/index.html", title=title, plugins=plugins, module_id=module_id)
    else:
        return render_template("luminus/index.html", title=title)


# PLUGIN ROUTES
@bp.route("/modules/<module_id>/announcements/")
@login_required
def module_plugin_announcements(module_id):
    module = Module.query.get_or_404(module_id)
    announcements = module.announcements.all()
    return render_template("luminus/plugins/announcements/index.html", announcements=announcements)


@bp.route("/modules/<module_id>/tasks/")
@login_required
def module_plugin_tasks(module_id):
    module = Module.query.get_or_404(module_id)
    tasks = module.tasks.all()
    return render_template("luminus/plugins/tasks/index.html", tasks=tasks)


@bp.route("/modules/<module_id>/files/", defaults={"search_path": ""})
@bp.route("/modules/<module_id>/files/<path:search_path>")
@login_required
def module_plugin_files(module_id, search_path):
    # check for unauthorised access
    module = Module.query.get_or_404(module_id)
    if module not in current_user.get_current_modules():
        abort(404)

    # get paths
    files_dir = os.path.join(os.path.abspath(os.path.dirname(__name__)), "webapp", "luminus", "modules", module_id, "files")
    path = os.path.join(files_dir, search_path)

    # download if path is a file
    if os.path.isfile(path):
        return send_file(path, as_attachment=True)

    # list contents if path is a directory
    breadcrumbs = []
    files = []
    dirs = []
    test_path = ""
    path_segments = os.path.join("files", search_path).split(os.path.sep)
    for index, path_segment in enumerate(path_segments):
        if index > 0:
            breadcrumb_path = url_for("luminus.module_plugin_files", module_id=module_id, search_path=test_path)
        else:
            breadcrumb_path = url_for("luminus.module_plugin_files", module_id=module_id, search_path="")

        breadcrumbs.append({
            "name": path_segment,
            "path": breadcrumb_path
        })

        test_path = os.path.join(test_path, path_segments[index - 1])

    for entry in os.listdir(path):
        item = {
            "name": entry,
            "path": os.path.join(search_path, entry)
        }
        if os.path.isfile(os.path.join(path, entry)):
            files.append(item)
        else:
            dirs.append(item)

    return render_template("luminus/plugins/files/index.html", breadcrumbs=breadcrumbs, dirs=dirs, files=files)