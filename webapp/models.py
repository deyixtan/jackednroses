# webapp/models.py
from flask_login import UserMixin
from webapp import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash

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
    enrolled = db.relationship('Enrolled', backref = 'user', uselist = False)

    def __init__(self, name, nusnetid, password, email):
        self.name = name
        self.nusnetid = nusnetid
        self.password_hash = generate_password_hash(password)
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Module(db.Model):
    __tablename__ = "modules"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    academic_year = db.Column(db.String(9))
    semester = db.Column(db.Integer())
    enrolled = db.relationship('Enrolled', backref = 'module', uselist = False)
    
    def __init__(self, code, name, academic_year, semester):
        self.code = code
        self.name = name
        self.academic_year = academic_year
        self.semester = semester
        
class Enrolled(db.Model):
    __tablename__ = "enrolled"
    #id = db.Column(db.Integer, primary_key=True)
    nusnetid = db.Column(db.String(64), db.ForeignKey('users.nusnetid'), primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), primary_key=True)

    def __init__(self, nusnetid, code, academic_year, semester):
        self.nusnetid = nusnetid
        module = Module.query.filter_by(code = code, academic_year = academic_year, semester = semester).first()
        self.module_id = module.id
    
    def __repr__(self):
        return f"<Module {self.module_id}>"