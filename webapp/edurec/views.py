# webapp/edurec/views.py
from flask_login import login_required
from webapp.edurec import edurec

@edurec.route("/")
@login_required
def index():
    return "Hello EduREC"
