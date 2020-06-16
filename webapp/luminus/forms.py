# webapp/luminus/forms.py
from flask_wtf import FlaskForm
from webapp.models import Module, Enrolled, User
from wtforms import IntegerField, StringField, SubmitField, ValidationError
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
        if Module.query.filter_by(code=self.code.data, academic_year = self.academic_year.data, semester = self.semester.data).first():
            self.code.errors.append("Module, academic year and/or semester has already been registered!")
        if len(self.errors) == 0:
            return True
        return False

class EnrollToModuleForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    academic_year = StringField("Academic Year (eg. 2019/2020)", validators=[DataRequired()]) 
    semester = IntegerField("Semester", validators=[DataRequired()])
    nusnetid = StringField("NUSNET ID", validators=[DataRequired()])
    submit = SubmitField("Enroll to Module")

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