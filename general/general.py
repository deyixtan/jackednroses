from flask import Blueprint

general_bp = Blueprint("general_bp", __name__)

@general_bp.route("/")
def index():
    return "Hello General"