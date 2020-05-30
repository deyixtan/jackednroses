# webapp/luminus/forms.py
from flask_wtf import FlaskForm
from webapp.models import Module
from wtforms import IntegerField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired

class CreateModuleForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    academic_year = IntegerField("Academic Year", validators=[DataRequired()])
    semester = IntegerField("Semester", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_code(self, field):
        if Module.query.filter_by(code=field.data).first():
            raise ValidationError("The course code has been registered already!")
