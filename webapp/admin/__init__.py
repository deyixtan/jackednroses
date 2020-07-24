from flask import Blueprint

bp = Blueprint("admin", __name__, template_folder="templates")

from webapp.admin import routes, hostel, module, user
