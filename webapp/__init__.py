# webapp/__init__.py
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "users.login"
bootstrap = Bootstrap()

def create_app(config_class=Config):
    # initialize app instance
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.globals.update(isinstance=isinstance)
    from webapp.models import Task, Exam
    app.jinja_env.globals.update(Task=Task)
    app.jinja_env.globals.update(Exam=Exam)

    # initialize flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    # blueprint registrations
    from webapp.admin.views import admin
    app.register_blueprint(admin, url_prefix="/admin")

    from webapp.api import api
    app.register_blueprint(api, url_prefix="/api")

    from webapp.core.views import core
    app.register_blueprint(core)

    from webapp.calendar.views import calendar
    app.register_blueprint(calendar, url_prefix="/calendar")
    
    from webapp.edurec.views import edurec
    app.register_blueprint(edurec, url_prefix="/edurec")

    from webapp.error_pages.handlers import error_pages
    app.register_blueprint(error_pages)

    from webapp.luminus.views import luminus
    app.register_blueprint(luminus, url_prefix="/luminus")

    from webapp.uhms.views import uhms
    app.register_blueprint(uhms, url_prefix="/uhms")

    from webapp.users.views import users
    app.register_blueprint(users)

    # return app instance
    return app
