from flask import Blueprint

bp = Blueprint("luminus", __name__)

from webapp.luminus import views
