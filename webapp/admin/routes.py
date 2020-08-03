from flask import abort, render_template, request, url_for
from flask_login import current_user, login_required
from webapp.admin import bp


@bp.before_request
def before_request():
    if not current_user:
        abort(404)
    if not current_user.is_admin:
        abort(404)


@bp.route("/")
@login_required
def index():
    page = request.args.get("page")
    if not page:
        return render_template("admin/index.html")
    page = url_for("admin." + str(page))
    return render_template("admin/index.html", page=page)
