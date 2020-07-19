from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from webapp.models import User


class LoginForm(FlaskForm):
    nusnetid = StringField("NUSNET ID", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")
