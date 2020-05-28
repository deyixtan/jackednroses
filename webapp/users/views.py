# webapp/users/views.py
from flask import flash, redirect, render_template, request, url_for, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from webapp import db
from webapp.models import User
from webapp.users.forms import LoginForm, RegistrationForm

users = Blueprint("users", __name__)

@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)

                next = request.args.get("next")
                if next == None or not next[0] == '/':
                    next = url_for("core.index")
                return redirect(next)

        flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("core.index"))

@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash("Successfully registered account.", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)
