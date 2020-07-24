from flask import Blueprint

bp = Blueprint("uhms", __name__, template_folder="templates")

from webapp.uhms import routes
