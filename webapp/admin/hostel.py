from flask import current_app, flash, redirect, request, render_template, url_for
from flask_login import login_required
from webapp import db, telegram
from webapp.admin import bp
from webapp.admin.forms import BroadcastMessageForm, CreateHostelForm, CreateRoomForm, DeleteBroadcastMessageForm, DeleteHostelForm, DeleteRoomForm, ManageApplicationForm
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


@bp.route("/hostel/delete_hostel", methods=["GET", "POST"])
@login_required
def delete_hostel():
    form = DeleteHostelForm()
    hostels = Hostel.query.all()
    hostels = [(hostel.id, hostel.name) for hostel in hostels]
    form.hostel_id.choices = hostels
    if form.validate_on_submit():
        # delete application
        HostelApplication.query.filter_by(hostel_id=form.hostel_id.data).delete()
        # delete messages
        HostelMessage.query.filter_by(hostel_id=form.hostel_id.data).delete()       
        # delete rooms
        HostelRoom.query.filter_by(hostel_id=form.hostel_id.data).delete() 
        # hostel
        Hostel.query.filter_by(id=form.hostel_id.data).delete()
        db.session.commit()
        flash("Successfully deleted hostel!", "success")
        return redirect(url_for("admin.delete_hostel"))
    return render_template("admin/hostel/delete_hostel.html", form=form)


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


@bp.route("/hostel/delete_room", methods=["GET", "POST"])
@login_required
def delete_room():
    form = DeleteRoomForm()
    rooms = HostelRoom.query.all()
    rooms = [(room.id, f"{room.hostel.name} Room {room.get_formatted_location()}") for room in rooms]
    form.room_id.choices = rooms
    if form.validate_on_submit():
        HostelRoom.query.get(form.room_id.data).delete()
        db.session.commit()
        flash("Successfully deleted hostel room!", "success")
        return redirect(url_for("admin.delete_room"))
    return render_template("admin/hostel/delete_room.html", form=form)


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

        user = User.query.get(form.user_id.data)
        if user.telegram_id:
            telegram.send_message(user.telegram_id, "Your hostel application has been approved.")
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

        hostel = Hostel.query.get(form.hostel_id.data)
        rooms = hostel.rooms
        for room in rooms:
            user = room.get_current_user()
            if user:
                if user.telegram_id:
                    telegram.send_message(user.telegram_id, f"There is a new message posted from {message.hostel.name}")
        flash("Successfully broadcasted message!", "success")
        return redirect(url_for("admin.broadcast_message"))
    return render_template("admin/hostel/broadcast_message.html", form=form)


@bp.route("/hostel/delete_broadcast_message", methods=["GET", "POST"])
@login_required
def delete_broadcast_message():
    form = DeleteBroadcastMessageForm()
    messages = HostelMessage.query.all()
    messages = [(message.id, f"[{message.hostel.name}] {message.title}") for message in messages]
    form.message_id.choices = messages
    if form.validate_on_submit():
        HostelMessage.query.get(form.message_id.data).delete()
        db.session.commit()

        flash("Successfully deleted broadcasted message!", "success")
        return redirect(url_for("admin.delete_broadcast_message"))
    return render_template("admin/hostel/delete_broadcast_message.html", form=form)
