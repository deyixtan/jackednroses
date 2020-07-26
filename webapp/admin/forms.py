from flask_wtf import FlaskForm
from webapp.models import ModuleAnnouncement, ModuleTask, Module, User, UserProfile, Plugin
from wtforms import BooleanField, IntegerField, MultipleFileField, PasswordField, RadioField, SelectField, StringField, SubmitField, TextAreaField, ValidationError
from wtforms.fields.html5 import DateTimeLocalField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from datetime import datetime


class RegisterUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    verfiy_password = PasswordField("Verify Password", validators=[DataRequired(), EqualTo("password", message="Password must match.")])
    create_profile = BooleanField("Create empty profile")
    submit = SubmitField("Submit")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("The username is currently being used!")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("The email is currently being used!")


class CreateProfileForm(FlaskForm):
    user_id = SelectField("User", coerce=int, validators=[InputRequired()])
    nric = StringField("NRIC", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    gender = StringField("Gender", validators=[DataRequired()])
    birth_date = DateField("Birth Date", format="%Y-%m-%d")
    marital_status = StringField("Marital Status", validators=[DataRequired()])
    nationality = StringField("Nationality", validators=[DataRequired()])
    mobile_number = IntegerField("Mobile Number", validators=[DataRequired()])
    home_number = IntegerField("Home Number", validators=[DataRequired()])
    home_address = TextAreaField("Home Address", validators=[DataRequired()])
    emergency_contact_name = StringField("Emergency Contact Name", validators=[DataRequired()])
    emergency_contact_number = IntegerField("Emergency Contact Number", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_nric(self, field):
        if UserProfile.query.filter_by(nric=field.data).first():
            raise ValidationError("The NRIC is currently being used!")


class CreateModuleForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    academic_year = IntegerField("Academic Year", validators=[DataRequired()])
    semester = IntegerField("Semester", validators=[DataRequired()])
    submit = SubmitField("Submit")


class EnrollStudentForm(FlaskForm):
    module_id = SelectField("Module", coerce=int, validators=[InputRequired()])
    user_id = SelectField("User", coerce=int, validators=[InputRequired()])
    submit = SubmitField("Submit")


class PostAnnouncementForm(FlaskForm):
    module_id = SelectField("Module", coerce=int, validators=[InputRequired()])
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PostTaskForm(FlaskForm):
    module_id = SelectField("Module", coerce=int, validators=[InputRequired()])
    start_timestamp = DateTimeLocalField("Start", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    end_timestamp = DateTimeLocalField("End", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AssignTaskForm(FlaskForm):
    task_id = SelectField("Task", coerce=int, validators=[InputRequired()])
    user_id = SelectField("User", coerce=int, validators=[InputRequired()])
    info = StringField("Specific User Info")
    submit = SubmitField("Submit")


class UploadFilesForm(FlaskForm):
    module_id = SelectField("Module", coerce=int, validators=[InputRequired()])
    category = SelectField("Category", choices=[("labs", "Labs"), ("lectures", "Lectures"), ("tutorials", "Tutorials"), ("misc", "Misc")], validators=[InputRequired()])
    files = MultipleFileField('File(s) Upload')
    submit = SubmitField("Submit")


class TogglePluginForm(FlaskForm):
    module_id = SelectField("Module", coerce=int, validators=[InputRequired()])
    plugin_id = SelectField("Plugin", coerce=int, validators=[InputRequired()])
    toggle = RadioField("Toggle", coerce=int, choices=[(1, "Enable"), (0, "Disable")])
    submit = SubmitField("Submit")


class CreateHostelForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    type = StringField("Type", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CreateRoomForm(FlaskForm):
    hostel_id = SelectField("Hostel", coerce=int, validators=[InputRequired()])
    block = StringField("Block", validators=[DataRequired()])
    level = StringField("Level", validators=[DataRequired()])
    room = StringField("Room", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ManageApplicationForm(FlaskForm):
    user_id = SelectField("User", coerce=int, validators=[InputRequired()])
    hostel_room_id = SelectField("Room", coerce=int, validators=[InputRequired()])
    submit = SubmitField("Submit")


class BroadcastMessageForm(FlaskForm):
    hostel_id = SelectField("Hostel", coerce=int, validators=[InputRequired()])
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Submit")


class TelegramBotForm(FlaskForm):
    toggle = RadioField("Toggle", coerce=int, choices=[(1, "Enable"), (0, "Disable")])
    submit = SubmitField("Submit")
