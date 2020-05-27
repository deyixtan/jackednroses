from flask import Blueprint

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/")
def index():
    return "Hello Auth"
