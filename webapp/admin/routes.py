from flask import render_template, request, url_for
from flask_login import login_required
from webapp.admin import bp


@bp.route("/")
@login_required
def index():
    page = request.args.get("page")
    if not page:
        return render_template("admin/index.html")
    page = url_for("admin." + str(page))
    return render_template("admin/index.html", page=page)
