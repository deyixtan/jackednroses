from flask import Blueprint

bp = Blueprint("users", __name__)

from webapp.users import routes
