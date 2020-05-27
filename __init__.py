import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from jackednroses.auth.auth import auth_bp
from jackednroses.edurec.edurec import edurec_bp
from jackednroses.general.general import general_bp
from jackednroses.luminus.luminus import luminus_bp
from jackednroses.uhms.uhms import uhms_bp


# Set up Application
app = Flask(__name__)

# Set up SQLAlchemy for Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create Database with Migration capabilities
db = SQLAlchemy(app)
Migrate(app, db)

# Registering Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth") # Authentication
app.register_blueprint(edurec_bp, url_prefix="/edurec") # EduREC
app.register_blueprint(general_bp, url_prefix="/general") # General
app.register_blueprint(luminus_bp, url_prefix="/luminus") # LumiNUS
app.register_blueprint(uhms_bp, url_prefix="/uhms") # UHMS
