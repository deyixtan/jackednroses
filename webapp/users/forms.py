# webapp/users/forms.py
from flask_wtf import FlaskForm
from webapp.models import User
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Password must match.")])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Register")

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered already!")

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Your username has been registered already!")
