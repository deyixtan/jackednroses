from flask import Blueprint, render_template


general_bp = Blueprint("general_bp", __name__, template_folder="templates")

@general_bp.route("/")
def index():
    return render_template("index.html")

@general_bp.route("/profile")
def profile():
    return render_template("profile.html")