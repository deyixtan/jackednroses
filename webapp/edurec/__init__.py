from flask import Blueprint

bp = Blueprint("edurec", __name__)

from webapp.edurec import views
