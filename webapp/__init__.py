# webapp/__init__.py
import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Set up Application
app = Flask(__name__)

# App Path & Configurations
basedir =  os.path.abspath(os.path.dirname(__name__))
app.config["SECRET_KEY"] = "jackednroses"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set up SQLAlchemy & Database migration capabilities
db = SQLAlchemy(app)
Migrate(app, db)

# Set up LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

# Registering Blueprints
from webapp.core.views import core
from webapp.edurec.views import edurec
from webapp.error_pages.handlers import error_pages
from webapp.luminus.views import luminus
from webapp.uhms.views import uhms
from webapp.users.views import users
app.register_blueprint(core)
app.register_blueprint(edurec, url_prefix="/edurec")
app.register_blueprint(error_pages)
app.register_blueprint(luminus, url_prefix="/luminus")
app.register_blueprint(uhms, url_prefix="/uhms")
app.register_blueprint(users)
