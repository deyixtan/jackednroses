# webapp/uhms/views.py
from flask_login import login_required
from webapp.uhms import uhms

@uhms.route("/")
@login_required
def index():
    return "Hello UHMS"
