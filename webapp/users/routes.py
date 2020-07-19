from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from webapp import db
from webapp.models import User
from webapp.users import bp
from webapp.users.forms import LoginForm


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nusnetid=form.nusnetid.data).first()
        if user is not None or not user.check_password(form.password.data):
            flash("Invalid NUSNET ID or password")
            return redirect(url_for("users.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("core.index"))
