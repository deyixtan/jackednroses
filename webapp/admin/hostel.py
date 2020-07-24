from flask import current_app, flash, redirect, request, render_template, url_for
from flask_login import login_required
from webapp import db
from webapp.admin import bp
from webapp.admin.forms import BroadcastMessageForm, CreateHostelForm, CreateRoomForm, ManageApplicationForm
from webapp.models import Hostel, HostelApplication, HostelMessage, HostelRoom, HostelRoomUserMap, User


@bp.route("/hostel/create_hostel", methods=["GET", "POST"])
@login_required
def create_hostel():
    form = CreateHostelForm()
    if form.validate_on_submit():
        hostel = Hostel.query.filter_by(name=form.name.data).first()
        if hostel:
            flash("This hostel already exist!", "danger")
            return redirect(url_for("admin.create_hostel"))
        hostel = Hostel()
        form.populate_obj(hostel)
        db.session.add(hostel)
        db.session.commit()
        flash("Successfully created hostel!", "success")
        return redirect(url_for("admin.create_hostel"))
    return render_template("admin/hostel/create_hostel.html", form=form)


@bp.route("/hostel/create_room", methods=["GET", "POST"])
@login_required
def create_room():
    form = CreateRoomForm()
    hostels = Hostel.query.all()
    hostels = [(hostel.id, hostel.name) for hostel in hostels]
    form.hostel_id.choices = hostels
    if form.validate_on_submit():
        room = HostelRoom.query.filter_by(hostel_id=form.hostel_id.data, block=form.block.data, level=form.level.data, room=form.room.data).first()
        if room:
            flash("This hostel room already exist!", "danger")
            return redirect(url_for("admin.create_room"))
        room = HostelRoom()
        form.populate_obj(room)
        db.session.add(room)
        db.session.commit()
        flash("Successfully created hostel room!", "success")
        return redirect(url_for("admin.create_room"))
    return render_template("admin/hostel/create_room.html", form=form)


@bp.route("/hostel/manage_application", methods=["GET", "POST"])
@login_required
def manage_application():
    form = ManageApplicationForm()
    applications = HostelApplication.query.all()
    user_ids = []
    hostel_room_ids = []
    for application in applications:
        user_id = application.user_id
        username = User.query.get(application.user_id).username
        user_ids.append((user_id, username))

        hostel_id = application.hostel_id
        rooms = Hostel.query.get(hostel_id).rooms
        for room in rooms:
            if room.is_currently_available():
                room_option = (room.id, f"[{room.hostel.name.capitalize()}] Room {room.get_formatted_location()}")
                if room_option not in hostel_room_ids:
                    hostel_room_ids.append(room_option)

    form.user_id.choices = user_ids
    form.hostel_room_id.choices = hostel_room_ids
    if form.validate_on_submit():
        application = HostelApplication.query.filter_by(user_id=form.user_id.data, hostel_id=HostelRoom.query.get(form.hostel_room_id.data).hostel.id).first()
        db.session.delete(application)
        rent = HostelRoomUserMap(hostel_room_id=form.hostel_room_id.data, academic_year=current_app.config["CURRENT_ACADEMIC_YEAR"], semester=current_app.config["CURRENT_SEMESTER"], user_id=form.user_id.data)
        db.session.add(rent)
        db.session.commit()
        flash("Successfully processed application!", "success")
        return redirect(url_for("admin.manage_application"))
    return render_template("admin/hostel/manage_application.html", form=form)


@bp.route("/hostel/broadcast_message", methods=["GET", "POST"])
@login_required
def broadcast_message():
    form = BroadcastMessageForm()
    hostels = Hostel.query.all()
    hostels = [(hostel.id, hostel.name) for hostel in hostels]
    form.hostel_id.choices = hostels
    if form.validate_on_submit():
        message = HostelMessage()
        form.populate_obj(message)
        db.session.add(message)
        db.session.commit()
        flash("Successfully broadcasted message!", "success")
        return redirect(url_for("admin.broadcast_message"))
    return render_template("admin/hostel/broadcast_message.html", form=form)
