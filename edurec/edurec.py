from flask import Blueprint

edurec_bp = Blueprint("edurec_bp", __name__)

@edurec_bp.route("/")
def index():
    return "Hello EduREC"
