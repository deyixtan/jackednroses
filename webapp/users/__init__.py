# webapp/users/__init__.py
from flask import Blueprint

users = Blueprint("users", __name__)

from webapp.users import views
