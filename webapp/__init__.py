from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "users.login"
bootstrap = Bootstrap()
moment = Moment()


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
    moment.init_app(app)

    # blueprint registrations
    from webapp.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from webapp.core import bp as core_bp
    app.register_blueprint(core_bp)

    from webapp.calendar import bp as calendar_bp
    app.register_blueprint(calendar_bp, url_prefix="/calendar")

    from webapp.edurec import bp as edurec_bp
    app.register_blueprint(edurec_bp, url_prefix="/edurec")

    from webapp.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from webapp.luminus import bp as luminus_bp
    app.register_blueprint(luminus_bp, url_prefix="/luminus")

    from webapp.uhms import bp as uhms_bp
    app.register_blueprint(uhms_bp, url_prefix="/uhms")

    from webapp.users import bp as users_bp
    app.register_blueprint(users_bp)

    # return app instance
    return app
