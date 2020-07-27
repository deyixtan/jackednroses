from flask import flash, redirect, render_template, url_for
from flask_login import login_required
from webapp import db
from webapp.admin import bp
from webapp.admin.forms import CreateProfileForm, DeleteProfileForm, RegisterUserForm, UnregisterUserForm
from webapp.models import HostelApplication, User, UserProfile


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


@bp.route("/user/unregister_user", methods=["GET", "POST"])
@login_required
def unregister_user():
    form = UnregisterUserForm()
    users = User.query.all()
    users = [(user.id, user.username) for user in users]
    form.user_id.choices = users
    if form.validate_on_submit():
        # hostel application
        HostelApplication.query.filter_by(user_id=form.user_id.data).delete()
        # delete profile
        UserProfile.query.filter_by(user_id=form.user_id.data).delete()
        # delete user
        User.query.filter_by(id=form.user_id.data).delete()
        db.session.commit()
        flash("Successfully unregistered user!", "success")
        return redirect(url_for("admin.unregister_user"))
    return render_template("admin/user/unregister_user.html", form=form)


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


@bp.route("/user/delete_profile", methods=["GET", "POST"])
@login_required
def delete_profile():
    form = DeleteProfileForm()
    profiles = UserProfile.query.all()
    profiles = [(profile.id, profile.get_full_name()) for profile in profiles]
    form.profile_id.choices = profiles
    if form.validate_on_submit():
        UserProfile.query.filter_by(id=form.profile_id.data).delete()
        db.session.commit()
        flash("Successfully deleted profile!", "success")
        return redirect(url_for("admin.delete_profile"))
    return render_template("admin/user/delete_profile.html", form=form)