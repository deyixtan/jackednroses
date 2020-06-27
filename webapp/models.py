# webapp/models.py
from flask_login import UserMixin
from webapp import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash
import datetime, pytz


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    nusnetid = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    profile_img = db.Column(db.String(20), nullable=False, default="default_profile.png")
    enrolled = db.relationship('Enrolled', backref = 'user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.id}>"


class Module(db.Model):
    __tablename__ = "modules"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64))
    academic_year = db.Column(db.String(9))
    semester = db.Column(db.Integer())
    enrolled = db.relationship('Enrolled', backref = 'module')
    announcements = db.relationship('Announcement', backref = 'module')
    tasks = db.relationship('Task', backref = 'module')
    exams = db.relationship('Exam', backref = 'module')

    def __repr__(self):
        return f"<Module {self.id}>"      


class Enrolled(db.Model):
    __tablename__ = "enrolled"
    #id = db.Column(db.Integer, primary_key=True)
    nusnetid = db.Column(db.String(64), db.ForeignKey('users.nusnetid'), primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), primary_key=True)

    def set_module(self, code, academic_year, semester):
        self.module_id = Module.query.filter_by(code = code, academic_year = academic_year, semester = semester).first().id

    def __repr__(self):
        return f"<Module {self.module_id}, {self.nusnetid}>"


class Announcement(db.Model):
    __tablename__ = "announcements"
    id = db.Column(db.Integer, primary_key = True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'))
    date = db.Column(db.DateTime)
    title = db.Column(db.String(32))
    body = db.Column(db.String(1024))

    def set_module(self, code, academic_year, semester):
        self.module_id = Module.query.filter_by(code = code, academic_year = academic_year, semester = semester).first().id

    def set_timestamp(self):
        dt = datetime.datetime.now(tz=pytz.UTC)
        self.date = dt.astimezone(pytz.timezone('Asia/Singapore'))

    def __repr__(self):
        return f"<Announcement {self.id}, {self.module_id}, {self.title}, {self.date}"
    

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key = True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'))
    taskname = db.Column(db.String(32))
    taskinfo = db.Column(db.String(1024))
    timestamp = db.Column(db.DateTime)

    def set_module(self, code, academic_year, semester):
        self.module_id = Module.query.filter_by(code = code, academic_year = academic_year, semester = semester).first().id

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def __repr__(self):
        return f"<Task {self.id}, {self.module_id}, {self.taskname}, {self.date}"


class Exam(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key = True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'))
    examname = db.Column(db.String(32))
    examinfo = db.Column(db.String(1024))
    location = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime)
    examdetails = db.relationship('ExamDetails', backref = 'exam')

    def set_module(self, code, academic_year, semester):
        self.module_id = Module.query.filter_by(code = code, academic_year = academic_year, semester = semester).first().id

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp
    
    def __repr__(self):
        return f"<Exam {self.id}, {self.module_id}, {self.examname}, {self.examdatetime}"


class ExamDetails(db.Model):
    __tablename__ = "examdetails"
    nusnetid = db.Column(db.String(64), db.ForeignKey('users.nusnetid'), primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), primary_key=True)
    seatnum = db.Column(db.Integer)
    
    def set_exam(self, code, academic_year, semester):
        module_id = Module.query.filter_by(code = code, academic_year = academic_year, semester = semester).first().id
        self.exam_id = Exam.query.filter_by(module_id = module_id).first().id
    
    def __repr__(self):
        return f"<Exam Details {self.module_id}, {self.nusnetid}, {self.seatnum}>"
