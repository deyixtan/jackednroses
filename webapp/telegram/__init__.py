from flask import Blueprint

bp = Blueprint("telegram", __name__, template_folder="templates")

from webapp.telegram import routes
