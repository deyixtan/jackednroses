from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired


class CreateApplicationForm(FlaskForm):
    hostel = SelectField("Hostel Type", coerce=int, validators=[InputRequired()])
    submit = SubmitField("Apply")
