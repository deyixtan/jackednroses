from flask import Blueprint

bp = Blueprint("core", __name__)

from webapp.core import views
