from flask import jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from webapp import db
from webapp.edurec import bp
from webapp.edurec.forms import UserDetailsCreateForm
from webapp.models import ModuleAnnouncement, ModuleTask, Module, User, Plugin, UHMSMessage


@bp.route("/")
@login_required
def index():
    # find user and userdetail object of user
    user = User.query.get(current_user.get_id())
    userdetails = UserDetails.query.filter_by(nusnetid=user.nusnetid).first()
    # if new user and no user details found
    if not userdetails:
        return redirect(url_for('edurec.update_information'))
    # user details exist
    else:
        # DICTIONARY WORK HERE
        userdict = {
            'name': user.name,
            'nusnetid': user.nusnetid,
            'email': user.email,
            'nric': userdetails.nric,
            'gender': userdetails.gender,
            'dob': userdetails.dob,
            'marital_status': userdetails.marital_status,
            'nationality': userdetails.nationality,
            'mobilenum': userdetails.mobilenum,
            'homenum': userdetails.homenum,
            'address': userdetails.address,
            'emergencycontactname': userdetails.emergencycontactname,
            'emergencycontactnum': userdetails.emergencycontactnum,
        }
        # return jsonify(userdict)
        return render_template('edurec/index.html', userdict=userdict)


@bp.route("/update", methods=["GET", "POST"])
@login_required
def update_information():
    form = UserDetailsCreateForm()
    userdetails = UserDetails.query.filter_by(nusnetid=User.query.get(current_user.get_id()).nusnetid).first()
    # if userdetails are present, auto fill for user to update
    if userdetails:
        form.nric.data = userdetails.nric
        userdetails.gender = form.gender.data = userdetails.gender
        form.dob.data = userdetails.dob
        form.marital_status.data = userdetails.marital_status
        form.nationality.data = userdetails.nationality
        form.mobilenum.data = userdetails.mobilenum
        form.homenum.data = userdetails.homenum
        form.address.data = userdetails.address
        form.emergencycontactname.data = userdetails.emergencycontactname
        form.emergencycontactnum.data = userdetails.emergencycontactnum
    if form.validate_on_submit():
        # if userdetails does not exist, add entry to table
        if not userdetails:
            userdetails = UserDetails(nusnetid=User.query.get(current_user.get_id()).nusnetid, nric=form.nric.data, gender=form.gender.data, dob=form.dob.data, marital_status=form.marital_status.data, nationality=form.nationality.data, mobilenum=form.mobilenum.data, homenum=form.homenum.data, address=form.address.data, emergencycontactname=form.emergencycontactname.data, emergencycontactnum=form.emergencycontactnum.data)
            db.session.add(userdetails)
        # if exist, update fields respectively
        else:
            userdetails.nusnetid = User.query.get(current_user.get_id()).nusnetid
            userdetails.nric = form.nric.data
            userdetails.gender = form.gender.data
            userdetails.dob = form.dob.data
            userdetails.marital_status = form.marital_status.data
            userdetails.nationality = form.nationality.data
            userdetails.mobilenum = form.mobilenum.data
            userdetails.homenum = form.homenum.data
            userdetails.address = form.address.data
            userdetails.emergencycontactname = form.emergencycontactname.data
            userdetails.emergencycontactnum = form.emergencycontactnum.data
        db.session.commit()
        flash("Successfully updated user information", "success")
        return redirect(url_for('edurec.index'))
    return render_template("edurec/update_information.html", form=form)
