# webapp/admin/views.py
import os
from flask import flash, render_template
from webapp import db
from webapp.admin import admin
from webapp.admin.forms import ModuleAnnoucementCreateForm, ModuleCreateForm, ModuleExamCreateForm, ModuleTaskCreateForm, ModuleUserCreateForm, UserCreateForm
from webapp.models import Announcement, Enrolled, Exam, Module, Task, User

@admin.route("/")
def index():
    return render_template("admin_index.html")


@admin.route("/module_annoucement_create", methods=["GET", "POST"])
def module_annoucement_create():
    form = ModuleAnnoucementCreateForm()
    if form.validate_on_submit():
        announcement = Announcement(title = form.title.data, body = form.body.data)
        announcement.set_module(form.code.data, form.academic_year.data, form.semester.data)
        announcement.set_timestamp()
        db.session.add(announcement)
        db.session.commit()
        flash("Successfully published announcement.", "success")   
    return render_template("admin_module_annoucement_create.html", form=form)


@admin.route("/module_create", methods=["GET", "POST"])
def module_create():
    form = ModuleCreateForm()
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
    return render_template("admin_module_create.html", form=form)


@admin.route("/module_exam_create", methods=["GET", "POST"])
def module_exam_create():
    form = ModuleExamCreateForm()
    if form.validate_on_submit():
        exam = Exam(examname = form.examname.data, examinfo = form.examinfo.data)
        exam.set_module(form.code.data, form.academic_year.data, form.semester.data)
        exam.set_timestamp(form.timestamp.data)
        db.session.add(exam)
        db.session.commit()
        flash("Successfully published exam details", "success")
    return render_template("admin_module_exam_create.html", form=form)


@admin.route("/module_task_create", methods=["GET", "POST"])
def module_task_create():
    form = ModuleTaskCreateForm()
    if form.validate_on_submit():
        task = Task(taskname = form.taskname.data, taskinfo = form.taskinfo.data)
        task.set_module(form.code.data, form.academic_year.data, form.semester.data)
        task.set_timestamp(form.timestamp.data)
        db.session.add(task)
        db.session.commit()
        flash("Successfully published task.", "success")
    return render_template("admin_module_task_create.html", form=form)


@admin.route("/module_user_create", methods=["GET", "POST"])
def module_user_create():
    form = ModuleUserCreateForm()
    if form.validate_on_submit():
        enrolled = Enrolled(nusnetid = form.nusnetid.data)
        enrolled.set_module(form.code.data, form.academic_year.data, form.semester.data)
        db.session.add(enrolled)
        db.session.commit()
        flash("Successfully enrolled student to module.", "success")
    return render_template("admin_module_user_create.html", form=form)
    

@admin.route("/user_create", methods=["GET", "POST"])
def user_create():
    form = UserCreateForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, nusnetid=form.nusnetid.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Successfully registered account.", "success")
    return render_template("admin_user_create.html", form=form)
