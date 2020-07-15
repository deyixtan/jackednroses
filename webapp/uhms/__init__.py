from flask import Blueprint

uhms = Blueprint("uhms", __name__)

from webapp.uhms import views
