# webapp/luminus/forms.py
from flask_wtf import FlaskForm
from webapp.models import Module, Enrolled, User, Announcement, Exam
from wtforms import IntegerField, StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired

class CreateModuleForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    academic_year = StringField("Academic Year (eg. 2019/2020)", validators=[DataRequired()])
    semester = IntegerField("Semester", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        mod = Module.query.filter_by(code=self.code.data, academic_year = self.academic_year.data, semester = self.semester.data).first()
        if mod:
            self.code.errors.append("Module, academic year and/or semester has already been registered!")
        if len(self.errors) == 0:
            return True
        return False

class EnrolToModuleForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    academic_year = StringField("Academic Year (eg. 2019/2020)", validators=[DataRequired()]) 
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
        mod = Module.query.filter_by(code=self.code.data, academic_year = self.academic_year.data, semester = self.semester.data).first()
        if not mod:
            self.code.errors.append("Module, Academic Year and/or semester does not exit!")
        if usr and mod:
            if Enrolled.query.filter_by(nusnetid=usr.nusnetid, module_id = mod.id).first():
                self.code.errors.append("Student has already been enrolled to module!")
        if len(self.errors) == 0:
            return True
        return False

class CreateAnnouncementForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    academic_year = StringField("Academic Year (eg. 2019/2020)", validators=[DataRequired()]) 
    semester = IntegerField("Semester", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Publish Announcement")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        mod = Module.query.filter_by(code=self.code.data, academic_year = self.academic_year.data, semester = self.semester.data).first()
        if not mod:
            self.code.errors.append("Module, Academic Year and/or semester does not exit!")
        if len(self.errors) == 0:
            return True
        return False

class CreateTaskForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    academic_year = StringField("Academic Year (eg. 2019/2020)", validators=[DataRequired()]) 
    semester = IntegerField("Semester", validators=[DataRequired()])
    taskname = StringField("Task Name", validators=[DataRequired()])
    taskinfo = TextAreaField("Task Info", validators=[DataRequired()])

    day = IntegerField("Date (DAY/MONTH/YEAR)", validators=[DataRequired()])
    month = IntegerField(validators=[DataRequired()])
    year = IntegerField(validators=[DataRequired()])

    hour = IntegerField("Time (HOUR:MINUTES)", validators=[DataRequired()])
    minute = IntegerField(validators=[DataRequired()])

    submit = SubmitField("Publish Task")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        mod = Module.query.filter_by(code=self.code.data, academic_year = self.academic_year.data, semester = self.semester.data).first()
        if not mod:
            self.code.errors.append("Module, Academic Year and/or semester does not exit!")
        if len(self.errors) == 0:
            return True
        return False

class CreateExamForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    academic_year = StringField("Academic Year (eg. 2019/2020)", validators=[DataRequired()]) 
    semester = IntegerField("Semester", validators=[DataRequired()])
    examname = StringField("Exam Name", validators=[DataRequired()])
    examinfo = TextAreaField("Exam Info", validators=[DataRequired()])

    day = IntegerField("Date (DAY/MONTH/YEAR)", validators=[DataRequired()])
    month = IntegerField(validators=[DataRequired()])
    year = IntegerField(validators=[DataRequired()])

    hour = IntegerField("Time (HOUR:MINUTES)", validators=[DataRequired()])
    minute = IntegerField(validators=[DataRequired()])

    submit = SubmitField("Publish Exam Details")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        mod = Module.query.filter_by(code=self.code.data, academic_year = self.academic_year.data, semester = self.semester.data).first()
        if not mod:
            self.code.errors.append("Module, Academic Year and/or semester does not exit!")
        if len(self.errors) == 0:
            return True
        return False