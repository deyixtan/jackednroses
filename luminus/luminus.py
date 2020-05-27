from flask import Blueprint

luminus_bp = Blueprint("luminus_bp", __name__)

@luminus_bp.route("/")
def index():
    return "Hello LumiNUS"