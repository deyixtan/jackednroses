# naming reference from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
from flask import render_template
from webapp import db
from webapp.errors import bp


@bp.app_errorhandler(403)
def forbidden(error):
    return (render_template("errors/403.html"), 403)


@bp.app_errorhandler(404)
def not_found(error):
    return (render_template("errors/404.html"), 404)


@bp.app_errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return (render_template("errors/500.html"), 500)
