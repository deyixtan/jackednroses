from flask import Blueprint

edurec = Blueprint("edurec", __name__)

from webapp.edurec import views
