from datetime import timezone
import os
from flask import flash, redirect, request, render_template, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename
from webapp import db
from webapp.admin import bp
from webapp.admin.forms import AssignTaskForm, CreateModuleForm, EnrollStudentForm, PostAnnouncementForm, PostTaskForm, TogglePluginForm, UploadFilesForm
from webapp.models import Module, ModuleAnnouncement, ModuleTask, ModuleTaskUserMap, Plugin, User


@bp.route("/module/create_module", methods=["GET", "POST"])
@login_required
def create_module():
    form = CreateModuleForm()
    if form.validate_on_submit():
        module = Module.query.filter_by(code=form.code.data, academic_year=form.academic_year.data, semester=form.semester.data).first()
        if module:
            flash("This module already exist!", "danger")
            return redirect(url_for("admin.create_module"))
        module = Module()
        form.populate_obj(module)
        db.session.add(module)
        db.session.commit()

        basedir = os.path.abspath(os.path.dirname(__name__))
        module_files_path = os.path.join(basedir, "webapp", "luminus", "modules", str(module.id), "files")
        if not os.path.exists(module_files_path):
            os.makedirs(os.path.join(module_files_path, "labs"))
            os.makedirs(os.path.join(module_files_path, "lectures"))
            os.makedirs(os.path.join(module_files_path, "tutorials"))
            os.makedirs(os.path.join(module_files_path, "misc"))

        flash("Successfully created module!", "success")
        return redirect(url_for("admin.create_module"))
    return render_template("admin/module/create_module.html", form=form)


@bp.route("/module/enroll_student", methods=["GET", "POST"])
@login_required
def enroll_student():
    form = EnrollStudentForm()
    modules = Module.query.all()
    modules = [(module.id, module.get_full_formatted()) for module in modules]
    form.module_id.choices = modules
    users = User.query.all()
    users = [(user.id, user.username) for user in users]
    form.user_id.choices = users
    if form.validate_on_submit():
        module = Module.query.get(form.module_id.data)
        user = User.query.get(form.user_id.data)
        if user in module.users.all():
            flash("This user is already enrolled to module!", "danger")
            return redirect(url_for("admin.enroll_student"))
        module.users.append(user)
        db.session.commit()
        flash("Successfully enrolled student!", "success")
        return redirect(url_for("admin.enroll_student"))
    return render_template("admin/module/enroll_student.html", form=form)


@bp.route("/module/post_announcement", methods=["GET", "POST"])
@login_required
def post_announcement():
    form = PostAnnouncementForm()
    modules = Module.query.all()
    modules = [(module.id, module.get_full_formatted()) for module in modules]
    form.module_id.choices = modules
    if form.validate_on_submit():
        announcement = ModuleAnnouncement()
        form.populate_obj(announcement)
        db.session.add(announcement)
        db.session.commit()
        flash("Successfully posted announcement!", "success")
        return redirect(url_for("admin.post_announcement"))
    return render_template("admin/module/post_announcement.html", form=form)


@bp.route("/module/post_task", methods=["GET", "POST"])
@login_required
def post_task():
    form = PostTaskForm()
    modules = Module.query.all()
    modules = [(module.id, module.get_full_formatted()) for module in modules]
    form.module_id.choices = modules
    if form.validate_on_submit():
        form.start_timestamp.data = form.start_timestamp.data.astimezone().astimezone(timezone.utc).replace(tzinfo=None)
        form.end_timestamp.data = form.end_timestamp.data.astimezone().astimezone(timezone.utc).replace(tzinfo=None)
        task = ModuleTask()
        form.populate_obj(task)
        db.session.add(task)
        db.session.commit()
        flash("Successfully posted task!", "success")
        return redirect(url_for("admin.post_task"))
    return render_template("admin/module/post_task.html", form=form)


@bp.route("/module/assign_task", methods=["GET", "POST"])
@login_required
def assign_task():
    form = AssignTaskForm()
    tasks = ModuleTask.query.all()
    tasks = [(task.id, f"{task.module.get_full_formatted()}, {task.title}") for task in tasks]
    form.task_id.choices = tasks
    users = User.query.all()
    users = [(user.id, user.username) for user in users]
    form.user_id.choices = users
    if form.validate_on_submit():
        task = ModuleTask.query.get(form.task_id.data)
        user = User.query.get(form.user_id.data)
        if user in task.users.all():
            flash("This task is already assigned to the user!", "danger")
            return redirect(url_for("admin.assign_task"))
        module_task_user = ModuleTaskUserMap()
        form.populate_obj(module_task_user)
        db.session.add(module_task_user)
        db.session.commit()
        flash("Successfully assigned task!", "success")
        return redirect(url_for("admin.assign_task"))
    return render_template("admin/module/assign_task.html", form=form)


@bp.route("module/upload_files", methods=["GET", "POST"])
@login_required
def upload_files():
    form = UploadFilesForm()
    modules = Module.query.all()
    modules = [(module.id, module.get_full_formatted()) for module in modules]
    form.module_id.choices = modules
    if form.validate_on_submit():
        basedir = os.path.abspath(os.path.dirname(__name__))
        module_files_path = os.path.join(basedir, "webapp", "luminus", "modules", str(form.module_id.data), "files")
        files = request.files.getlist(form.files.name)
        if files:
            for file in files:
                file.save(os.path.join(module_files_path, form.category.data, secure_filename(file.filename)))
        flash("Successfully uploaded file(s)", "success")
        return redirect(url_for("admin.upload_files"))
    return render_template("admin/module/upload_files.html", form=form)


@bp.route("module/toggle_plugin", methods=["GET", "POST"])
@login_required
def toggle_plugin():
    form = TogglePluginForm()
    modules = Module.query.all()
    modules = [(module.id, module.get_full_formatted()) for module in modules]
    form.module_id.choices = modules
    plugins = Plugin.query.all()
    plugins = [(plugin.id, plugin.name.capitalize()) for plugin in plugins]
    form.plugin_id.choices = plugins
    if form.validate_on_submit():
        module = Module.query.get(form.module_id.data)
        plugin = Plugin.query.get(form.plugin_id.data)
        if form.toggle.data:
            module.plugins.append(plugin)
        else:
            module.plugins.remove(plugin)
        db.session.commit()
        flash("Successfully toggled plugin!", "success")
        return redirect(url_for("admin.toggle_plugin"))
    return render_template("admin/module/toggle_plugin.html", form=form)
