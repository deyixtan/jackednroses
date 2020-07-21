from flask_wtf import FlaskForm
from webapp.models import ModuleAnnouncement, ModuleTask, Module, User, Plugin, UHMSMessage
from wtforms import IntegerField, PasswordField, StringField, SubmitField, TextAreaField, ValidationError
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, EqualTo


class ModuleAnnouncementCreateForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    academic_year = StringField("Academic Year", render_kw={"placeholder": "eg. 2019/2020"}, validators=[DataRequired()])
    semester = IntegerField("Semester", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", render_kw={"rows": 10}, validators=[DataRequired()])
    submit = SubmitField("Publish Announcement")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        mod = Module.query.filter_by(code=self.code.data, academic_year=self.academic_year.data, semester=self.semester.data).first()
        if not mod:
            self.code.errors.append("Module, Academic Year and/or semester does not exit!")
        if len(self.errors) == 0:
            return True
        return False


class ModuleCreateForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    academic_year = StringField("Academic Year", render_kw={"placeholder": "eg. 2019/2020"}, validators=[DataRequired()])
    semester = IntegerField("Semester", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        mod = Module.query.filter_by(code=self.code.data, academic_year=self.academic_year.data, semester=self.semester.data).first()
        if mod:
            self.code.errors.append("Module, academic year and/or semester has already been registered!")
        if len(self.errors) == 0:
            return True
        return False


class ModuleExamCreateForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    academic_year = StringField("Academic Year", render_kw={"placeholder": "eg. 2019/2020"}, validators=[DataRequired()])
    semester = IntegerField("Semester", validators=[DataRequired()])
    examname = StringField("Exam Name", validators=[DataRequired()])
    examinfo = TextAreaField("Exam Info", render_kw={"rows": 10}, validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    timestamp = DateTimeLocalField("Date", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    submit = SubmitField("Publish Exam Details")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        mod = Module.query.filter_by(code=self.code.data, academic_year=self.academic_year.data, semester=self.semester.data).first()
        if not mod:
            self.code.errors.append("Module, Academic Year and/or semester does not exit!")
        if len(self.errors) == 0:
            return True
        return False


class ModuleExamUserCreateForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    academic_year = StringField("Academic Year", render_kw={"placeholder": "eg. 2019/2020"}, validators=[DataRequired()])
    semester = IntegerField("Semester", validators=[DataRequired()])
    nusnetid = StringField("NUSNET ID", validators=[DataRequired()])
    seatnum = IntegerField("Seat Number", validators=[DataRequired()])
    submit = SubmitField("Enrol to Module")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        mod = Module.query.filter_by(code=self.code.data, academic_year=self.academic_year.data, semester=self.semester.data).first()
        if not mod:
            self.code.errors.append("Module, Academic Year and/or semester does not exist!")
        exam = Exam.query.filter_by(id=mod.id)
        if not exam:
            self.code.errors.append("Exam does not exist!")
        if len(self.errors) == 0:
            return True
        return False


class ModuleTaskCreateForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    academic_year = StringField("Academic Year", render_kw={"placeholder": "eg. 2019/2020"}, validators=[DataRequired()])
    semester = IntegerField("Semester", validators=[DataRequired()])
    taskname = StringField("Task Name", validators=[DataRequired()])
    taskinfo = TextAreaField("Task Info", render_kw={"rows": 10}, validators=[DataRequired()])
    timestamp = DateTimeLocalField("Due Date", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    submit = SubmitField("Publish Task")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        mod = Module.query.filter_by(code=self.code.data, academic_year=self.academic_year.data, semester=self.semester.data).first()
        if not mod:
            self.code.errors.append("Module, Academic Year and/or semester does not exit!")
        if len(self.errors) == 0:
            return True
        return False


class ModuleUserCreateForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    academic_year = StringField("Academic Year", render_kw={"placeholder": "eg. 2019/2020"}, validators=[DataRequired()])
    semester = IntegerField("Semester", validators=[DataRequired()])
    nusnetid = StringField("NUSNET ID", validators=[DataRequired()])
    submit = SubmitField("Enrol to Module")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        usr = User.query.filter_by(nusnetid=self.nusnetid.data).first()
        if not usr:
            self.nusnetid.errors.append("NUSNET ID does not exit!")
        mod = Module.query.filter_by(code=self.code.data, academic_year=self.academic_year.data, semester=self.semester.data).first()
        if not mod:
            self.code.errors.append("Module, Academic Year and/or semester does not exit!")
        if usr and mod:
            if Enrolled.query.filter_by(nusnetid=usr.nusnetid, module_id=mod.id).first():
                self.code.errors.append("Student has already been enrolled to module!")
        if len(self.errors) == 0:
            return True
        return False


class UserCreateForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    nusnetid = StringField("NUSNET ID", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Password must match.")])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered already!")

    def validate_nusnetid(self, field):
        if User.query.filter_by(nusnetid=field.data).first():
            raise ValidationError("Your nusnetid has been registered already!")

class UHMSMessageCreateForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", render_kw={"rows": 10}, validators=[DataRequired()])
    submit = SubmitField("Publish Message")