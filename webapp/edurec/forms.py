from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from webapp.models import UserProfile


class EditProfileForm(FlaskForm):
    nationality = StringField("Nationality", validators=[DataRequired()])
    nric = StringField("NRIC", validators=[DataRequired()])
    marital_status = StringField("Marital Status", validators=[DataRequired()])
    mobile_number = IntegerField("Mobile Number", validators=[DataRequired()])
    home_number = IntegerField("Home Number", validators=[DataRequired()])
    home_address = TextAreaField("Home Address", render_kw={"rows": 4}, validators=[DataRequired()])
    emergency_contact_name = StringField("Emergency Contact Name", validators=[DataRequired()])
    emergency_contact_number = IntegerField("Emergency Contact Number", validators=[DataRequired()])
    submit = SubmitField("Update Profile")

    def validate_nric(self, field):
        if UserProfile.query.filter_by(nric=field.data).first():
            raise ValidationError("The NRIC is currently being used!")
