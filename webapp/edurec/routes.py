from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from webapp import db
from webapp.edurec import bp
from webapp.edurec.forms import EditProfileForm


@bp.route("/")
@login_required
def index():
    return render_template("edurec/index.html")


@bp.route("/update", methods=["GET", "POST"])
@login_required
def update():
    form = EditProfileForm()
    if form.validate_on_submit():
        # update existing profile details with form changes
        current_user.profile.nationality = form.nationality.data
        current_user.profile.nric = form.nric.data
        current_user.profile.marital_status = form.marital_status.data
        current_user.profile.mobile_number = form.mobile_number.data
        current_user.profile.home_number = form.home_number.data
        current_user.profile.home_address = form.home_address.data
        current_user.profile.emergency_contact_name = form.emergency_contact_name.data
        current_user.profile.emergency_contact_number = form.emergency_contact_number.data
        db.session.commit()
        flash("Successfully updated user profile.", "success")
        return(redirect(url_for("edurec.index")))
    # prepopulate form with user existing profile details
    form.nationality.data = current_user.profile.nationality
    form.nric.data = current_user.profile.nric
    form.marital_status.data = current_user.profile.marital_status
    form.mobile_number.data = current_user.profile.mobile_number
    form.home_number.data = current_user.profile.home_number
    form.home_address.data = current_user.profile.home_address
    form.emergency_contact_name.data = current_user.profile.emergency_contact_name
    form.emergency_contact_number.data = current_user.profile.emergency_contact_number
    return render_template("edurec/update.html", form=form)
