from jackednroses import app
from flask import redirect, url_for


# Default route
@app.route("/")
def index():
    return redirect(url_for("general_bp.index"))
    