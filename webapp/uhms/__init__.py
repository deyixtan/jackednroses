from flask import Blueprint

bp = Blueprint("uhms", __name__)

from webapp.uhms import routes
