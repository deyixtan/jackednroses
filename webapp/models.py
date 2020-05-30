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
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    profile_img = db.Column(db.String(20), nullable=False, default="default_profile.png")
    
    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Module(db.Model):
    __tablename__ = "modules"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    academic_year = db.Column(db.Integer())
    semester = db.Column(db.Integer())
    
    def __init__(self, code, name, academic_year, semester):
        self.code = code
        self.name = name
        self.academic_year = academic_year
        self.semester = semester
        
