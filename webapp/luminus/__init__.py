from flask import Blueprint

bp = Blueprint("luminus", __name__, template_folder="templates")

from webapp.luminus import routes
