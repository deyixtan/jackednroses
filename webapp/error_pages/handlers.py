# webapp/error_pages/handlers.py
from flask import render_template, Blueprint
from webapp import db 

error_pages = Blueprint("error_pages", __name__)

@error_pages.app_errorhandler(403)
def error_403(error):
    return (render_template("error_pages/403.html"), 403)

@error_pages.app_errorhandler(404)
def error_404(error):
    return (render_template("error_pages/404.html"), 404)

@error_pages.app_errorhandler(500)
def error_500(error):
    db.session.rollback()
    return (render_template("error_pages/500.html"), 500)
