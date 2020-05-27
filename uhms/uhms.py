from flask import Blueprint

uhms_bp = Blueprint("uhms_bp", __name__)

@uhms_bp.route("/")
def index():
    return "Hello UHMS"