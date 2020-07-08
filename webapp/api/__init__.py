# webapp/api/__init__.py
from flask import Blueprint

api = Blueprint("api", __name__)

from webapp.api import users, modules
