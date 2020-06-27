# webapp/luminus/views.py
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from webapp import db
from webapp.luminus import luminus
from webapp.luminus.forms import CreateModuleForm, EnrolToModuleForm, CreateAnnouncementForm, CreateTaskForm, CreateExamForm, EnrolToExamForm
from webapp.models import Module, Enrolled, User, Announcement, Task, Exam, ExamDetails
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
    #Check if user has enrolled modules
    if enrolled:
        for mod in enrolled:
            module_list.append(Module.query.filter_by(id = mod.module_id).first())

        iframe = url_for('luminus.view_module', code=module_list[module_index].code)

        return render_template("luminus/index.html", module_list=module_list, iframe=iframe)
    else:
         return render_template("luminus/index.html")

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
        enrolled = Enrolled(nusnetid = form.nusnetid.data)
        enrolled.set_module(form.code.data, form.academic_year.data, form.semester.data)
        db.session.add(enrolled)
        db.session.commit()
        flash("Successfully enrolled student to module.", "success")
        return redirect(url_for("core.index"))
    return render_template("luminus/enrol_to_module.html", form=form)

@luminus.route("/create_announcement", methods=["GET", "POST"])
@login_required
def create_announcement():
    form = CreateAnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(title = form.title.data, body = form.body.data)
        announcement.set_module(form.code.data, form.academic_year.data, form.semester.data)
        announcement.set_timestamp()
        db.session.add(announcement)
        db.session.commit()
        flash("Successfully published announcement.", "success")
        return redirect(url_for("core.index"))
    return render_template("luminus/create_announcement.html", form=form)

@luminus.route("/create_task", methods=["GET", "POST"])
@login_required
def create_task():
    form = CreateTaskForm()
    if form.validate_on_submit():
        task = Task(taskname = form.taskname.data, taskinfo = form.taskinfo.data)
        task.set_module(form.code.data, form.academic_year.data, form.semester.data)
        task.set_timestamp(form.day.data, form.month.data, form.year.data, form.hour.data, form.minute.data)
        db.session.add(task)
        db.session.commit()
        flash("Successfully published task.", "success")
        return redirect(url_for("core.index"))
    return render_template("luminus/create_task.html", form=form)

@luminus.route("/create_exam", methods=["GET", "POST"])
@login_required
def create_exam():
    form = CreateExamForm()
    if form.validate_on_submit():
        exam = Exam(examname = form.examname.data, examinfo = form.examinfo.data, location = form.location.data)
        exam.set_module(form.code.data, form.academic_year.data, form.semester.data)
        exam.set_timestamp(form.day.data, form.month.data, form.year.data, form.hour.data, form.minute.data)
        db.session.add(exam)
        db.session.commit()
        flash("Successfully published exam details", "success")
        return redirect(url_for("core.index"))
    return render_template("luminus/create_exam.html", form=form)

@luminus.route("/enrol_to_exam", methods=["GET", "POST"])
@login_required
def enrol_to_exam():
    form = EnrolToExamForm()
    if form.validate_on_submit():
        examdetails = ExamDetails(nusnetid = form.nusnetid.data, seatnum = form.seatnum.data)
        examdetails.set_exam(form.code.data, form.academic_year.data, form.semester.data)
        db.session.add(examdetails)
        db.session.commit()
        flash("Successfully enrolled student to exam", "success")
        return redirect(url_for("core.index"))
    return render_template("luminus/enrol_to_exam.html", form=form)