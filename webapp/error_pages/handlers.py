# webapp/error_pages/handlers.py
# naming reference from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
from flask import render_template, Blueprint
from webapp import db

error_pages = Blueprint("error_pages", __name__)

@error_pages.app_errorhandler(403)
def forbidden(error):
    return (render_template("error_pages/403.html"), 403)

@error_pages.app_errorhandler(404)
def not_found(error):
    return (render_template("error_pages/404.html"), 404)

@error_pages.app_errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return (render_template("error_pages/500.html"), 500)
