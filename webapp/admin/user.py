from flask import flash, redirect, render_template, url_for
from flask_login import login_required
from webapp import db
from webapp.admin import bp
from webapp.admin.forms import CreateProfileForm, RegisterUserForm
from webapp.models import User, UserProfile


@bp.route("/user/register_user", methods=["GET", "POST"])
@login_required
def register_user():
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        if form.create_profile.data:
            user.profile = UserProfile()
        db.session.add(user)
        db.session.commit()
        flash("Successfully registered user!", "success")
        return redirect(url_for("admin.register_user"))
    return render_template("admin/user/register_user.html", form=form)


@bp.route("/user/create_profile", methods=["GET", "POST"])
@login_required
def create_profile():
    form = CreateProfileForm()
    # prepopulate selection field with users without profile
    users = User.query.filter_by(profile=None).all()
    users = [(user.id, user.username) for user in users]
    form.user_id.choices = users
    if form.validate_on_submit():
        profile = UserProfile()
        form.populate_obj(profile)
        db.session.add(profile)
        db.session.commit()
        flash("Successfully created profile!", "success")
        return redirect(url_for("admin.create_profile"))
    return render_template("admin/user/create_profile.html", form=form)
