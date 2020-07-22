from flask import Blueprint

bp = Blueprint("edurec", __name__, template_folder="templates")

from webapp.edurec import routes
