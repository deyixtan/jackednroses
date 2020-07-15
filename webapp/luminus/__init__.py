from flask import Blueprint

luminus = Blueprint("luminus", __name__)

from webapp.luminus import views
