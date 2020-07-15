from flask import Blueprint

core = Blueprint("core", __name__)

from webapp.core import views
