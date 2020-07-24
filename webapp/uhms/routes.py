from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from webapp import db
from webapp.models import Hostel, HostelApplication
from webapp.uhms import bp
from webapp.uhms.forms import CreateApplicationForm


@bp.route("/")
@login_required
def index():
    # get past accomodations
    past_rooms = current_user.get_past_hostel_rooms()
    # get current accomodations
    current_room = current_user.get_current_hostel_room()
    if not current_room:
        return render_template("uhms/index.html", past_rooms=past_rooms)
    # get messages from current accomodations
    messages = current_room.hostel.messages.all()
    return render_template("uhms/index.html", current_room=current_room, past_rooms=past_rooms, messages=messages)


@bp.route("/apply", methods=["GET", "POST"])
@login_required
def apply():
    form = CreateApplicationForm()
    # prepopulate selection field with hostels
    hostels = Hostel.query.all()
    hostels = [(hostel.id, f"{hostel.name.upper()} [{hostel.type.upper()}]") for hostel in hostels]
    form.hostel.choices = hostels
    # form submission
    if form.validate_on_submit():
        # check if user for existing hostel application
        application = HostelApplication.query.filter_by(user_id=current_user.id).first()
        if application:
            flash("You already have an application being processed.")
            return redirect(url_for("uhms.apply"))
        # create hostel application
        application = HostelApplication(user_id=current_user.id, hostel_id=form.hostel.data)
        db.session.add(application)
        db.session.commit()
        flash("Your hostel application is now being processed.")
        return redirect(url_for("uhms.index"))
    return render_template("uhms/apply.html", form=form)
