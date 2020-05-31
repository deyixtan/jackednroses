# webapp/users/forms.py
from flask_wtf import FlaskForm
from webapp.models import User
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    nusnetid = StringField("NUSNET ID", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class RegistrationForm(FlaskForm):
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
