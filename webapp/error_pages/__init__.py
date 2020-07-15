from flask import Blueprint

error_pages = Blueprint("error_pages", __name__)

from webapp.error_pages import handlers
