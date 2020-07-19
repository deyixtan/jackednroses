from flask_wtf import FlaskForm
from webapp.models import User, UserDetails
from wtforms import IntegerField, PasswordField, StringField, SubmitField, TextAreaField, ValidationError
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo


class UserDetailsCreateForm(FlaskForm):
    nric = StringField("NRIC", validators=[DataRequired()])
    gender = StringField("Gender", validators=[DataRequired()])
    dob = DateField("Date", format="%Y-%m-%d", validators=[DataRequired()])
    marital_status = StringField("Marital Status", validators=[DataRequired()])
    nationality = StringField("Nationality", validators=[DataRequired()])
    mobilenum = IntegerField("Mobile Number", validators=[DataRequired()])
    homenum = IntegerField("Home Number", validators=[DataRequired()])
    address = TextAreaField("Address", render_kw={"rows": 4}, validators=[DataRequired()])
    emergencycontactname = StringField("Emergency Contact Name", validators=[DataRequired()])
    emergencycontactnum = IntegerField("Emergency Contact Number", validators=[DataRequired()])
    submit = SubmitField("Update Information")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        mobnum = len(str(self.mobilenum.data))
        homenum = len(str(self.homenum.data))
        emnum = len(str(self.emergencycontactnum.data))
        if mobnum != 8 or homenum != 8 or emnum != 8:
            self.nric.errors.append("Phone numbers should be Singapore numbers only")
        if len(self.errors) == 0:
            return True
        return False
