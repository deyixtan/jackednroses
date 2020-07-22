import os
from flask import render_template, url_for, send_file, abort
from flask_login import current_user, login_required
from webapp.luminus import bp
from webapp.models import Module


@bp.route("/modules/<module_id>/announcements/")
@login_required
def module_plugin_announcements(module_id):
    # check for unauthorised access
    module = Module.query.get_or_404(module_id)
    if module not in current_user.get_current_modules():
        abort(404)
    # get all announcements
    announcements = module.get_announcements()
    return render_template("luminus/plugins/announcements/index.html", announcements=announcements)


@bp.route("/modules/<module_id>/tasks/")
@login_required
def module_plugin_tasks(module_id):
    # check for unauthorised access
    module = Module.query.get_or_404(module_id)
    if module not in current_user.get_current_modules():
        abort(404)
    # get all tasks
    tasks = module.get_tasks()
    return render_template("luminus/plugins/tasks/index.html", tasks=tasks)


@bp.route("/modules/<module_id>/files/", defaults={"search": ""})
@bp.route("/modules/<module_id>/files/<path:search>")
@login_required
def module_plugin_files(module_id, search):
    # check for unauthorised access
    module = Module.query.get_or_404(module_id)
    if module not in current_user.get_current_modules():
        abort(404)
    # get searched path
    searched_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "modules", module_id, "files", search)
    # check and download, if searched_path is a file
    if os.path.isfile(searched_path):
        return send_file(searched_path, as_attachment=True)
    # assume searched_path is a directory, and list the contents
    breadcrumbs = []
    dirs = []
    files = []
    # generate breadcrumbs from path
    looped_path = ""
    path_segments = os.path.join("files", search).split(os.path.sep)
    for index, path_segment in enumerate(path_segments):
        breadcrumb_path = url_for("luminus.module_plugin_files", module_id=module_id, search=looped_path)
        breadcrumbs.append({
            "name": path_segment,
            "path": breadcrumb_path
        })
        # append segment to looped_path
        looped_path = os.path.join(looped_path, path_segments[index - 1])
    # get directories and files in searched_path
    similar_files = {}
    for entry in os.listdir(searched_path):
        if os.path.isdir(os.path.join(searched_path, entry)):
            # get directories info
            dirs.append({
                "name": entry,
                "path": os.path.join(search, entry)
            })
        else:
            # get files info
            file_name = os.path.splitext(entry)[0]
            file_ext = os.path.splitext(entry)[1]
            if file_name not in similar_files:
                similar_files[file_name] = []
            # add files into similar_files dictionary
            similar_files[file_name].append({
                "path": os.path.join(search, entry),
                "ext": file_ext
            })
    # restructure similar_files dictionary into a proper list to render view
    for key, value in similar_files.items():
        files.append({
            "name": key,
            "info": value
        })
    return render_template("luminus/plugins/files/index.html", breadcrumbs=breadcrumbs, dirs=dirs, files=files)
