from flask import Blueprint

bp = Blueprint("calendar", __name__, template_folder="templates", static_folder="static", static_url_path="/admin/static")

from webapp.calendar import routes
