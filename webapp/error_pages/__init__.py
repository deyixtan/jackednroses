from flask import Blueprint

bp = Blueprint("error_pages", __name__)

from webapp.error_pages import handlers
