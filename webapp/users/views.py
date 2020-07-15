from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from webapp import db
from webapp.models import User
from webapp.users import users
from webapp.users.forms import LoginForm


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nusnetid=form.nusnetid.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)

                next = request.args.get("next")
                if next is None or not next[0] == '/':
                    next = url_for("core.index")
                return redirect(next)

        flash("Invalid NUSNET ID or password.", "danger")
    return render_template("login.html", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("core.index"))
