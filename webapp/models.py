from datetime import datetime
from sqlalchemy import and_, or_
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from webapp import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Association Tables
class ModuleUserMap(db.Model):
    __tablename__ = "module_user_map"
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)


class ModulePluginMap(db.Model):
    __tablename__ = "module_plugin_map"
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"), primary_key=True)
    plugin_id = db.Column(db.Integer, db.ForeignKey("plugin.id"), primary_key=True)


class ModuleTaskUserMap(db.Model):
    __tablename__ = "module_task_user_map"
    task_id = db.Column(db.Integer, db.ForeignKey("module_task.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    info = db.Column(db.String(1024))
    user = db.relationship("User", backref="module_task_user")
    module_tasks = db.relationship("ModuleTask", backref="module_task_user")


class HostelRoomUserMap(db.Model):
    __tablename__ = "hostel_room_user_map"
    hostel_room_id = db.Column(db.Integer, db.ForeignKey("hostel_room.id"), primary_key=True)
    academic_year = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="hostel_room_user")
    hostel_room = db.relationship("HostelRoom", backref="hostel_room_user")


# Object Tables
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    profile = db.relationship("UserProfile", backref="user", uselist=False, lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_current_modules(self):
        return self.modules.filter(and_(
            Module.academic_year == current_app.config["CURRENT_ACADEMIC_YEAR"],
            Module.semester == current_app.config["CURRENT_SEMESTER"]
        )).all()

    def get_tasks(self):
        return self.tasks.order_by(ModuleTask.start_timestamp.asc()).all()

    def get_current_tasks(self):
        return self.tasks.filter(ModuleTask.end_timestamp > datetime.utcnow()).order_by(ModuleTask.start_timestamp.asc()).all()

    def get_current_hostel_room(self):
        return self.hostel_rooms.filter(and_(
            HostelRoomUserMap.academic_year == current_app.config["CURRENT_ACADEMIC_YEAR"],
            HostelRoomUserMap.semester == current_app.config["CURRENT_SEMESTER"]
        )).first()

    def get_past_hostel_rooms(self):
        return db.session.query(Hostel, HostelRoom, HostelRoomUserMap).select_from(HostelRoomUserMap).join(User).join(HostelRoom).join(Hostel).filter(User.id == self.id).filter(or_(
            HostelRoomUserMap.academic_year != current_app.config["CURRENT_ACADEMIC_YEAR"],
            HostelRoomUserMap.semester != current_app.config["CURRENT_SEMESTER"]
        )).all()


class UserProfile(db.Model):
    __tablename__ = "user_profile"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    nric = db.Column(db.String(16), index=True, unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    gender = db.Column(db.String(16))
    birth_date = db.Column(db.Date)
    marital_status = db.Column(db.String(16))
    nationality = db.Column(db.String(32))
    mobile_number = db.Column(db.Integer)
    home_number = db.Column(db.Integer)
    home_address = db.Column(db.String(128))
    emergency_contact_name = db.Column(db.String(64))
    emergency_contact_number = db.Column(db.Integer)

    def __repr__(self):
        return f"<UserProfile {self.get_full_name()}>"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Module(db.Model):
    __tablename__ = "module"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64))
    academic_year = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    announcements = db.relationship("ModuleAnnouncement", backref="module", lazy="dynamic")
    tasks = db.relationship("ModuleTask", backref="module", lazy="dynamic")
    plugins = db.relationship(
        "Plugin", secondary=ModulePluginMap.__table__,
        primaryjoin="ModulePluginMap.module_id == Module.id",
        secondaryjoin="ModulePluginMap.plugin_id == Plugin.id",
        backref=db.backref("modules", lazy="dynamic"), lazy="dynamic"
    )
    users = db.relationship(
        "User", secondary=ModuleUserMap.__table__,
        primaryjoin="ModuleUserMap.module_id == Module.id",
        secondaryjoin="ModuleUserMap.user_id == User.id",
        backref=db.backref("modules", lazy="dynamic"), lazy="dynamic"
    )

    def __repr__(self):
        return f"<Module {self.code}>"

    def get_formatted_name(self):
        return f"[{self.code.upper()}] {self.name}"

    def get_announcements(self):
        return self.announcements.order_by(ModuleAnnouncement.timestamp.desc()).all()

    def get_tasks(self):
        return self.tasks.order_by(ModuleTask.start_timestamp.asc()).all()

    def get_current_tasks(self):
        return self.tasks.filter(ModuleTask.end_timestamp > datetime.utcnow()).order_by(ModuleTask.start_timestamp.asc()).all()

    def enable_plugin(self, plugin):
        if not self.is_plugin_enabled(plugin):
            self.plugins.append(plugin)
            db.session.commit()

    def disable_plugin(self, plugin):
        if self.is_plugin_enabled(plugin):
            self.plugins.remove(plugin)
            db.session.commit()

    def is_plugin_enabled(self, plugin):
        return self.plugins.filter(ModulePluginMap.plugin_id == plugin.id).count() > 0


class ModuleAnnouncement(db.Model):
    __tablename__ = "module_announcement"
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(32))
    body = db.Column(db.String(1024))

    def __repr__(self):
        return f"<ModuleAnnouncement {self.title}>"


class ModuleTask(db.Model):
    __tablename__ = "module_task"
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"))
    title = db.Column(db.String(32))
    body = db.Column(db.String(1024))
    start_timestamp = db.Column(db.DateTime)
    end_timestamp = db.Column(db.DateTime)
    location = db.Column(db.String(32))
    users = db.relationship(
        "User", secondary=ModuleTaskUserMap.__table__,
        backref=db.backref("tasks", lazy="dynamic"), lazy="dynamic"
    )

    def __repr__(self):
        return f"<ModuleTask {self.title}>"


class Plugin(db.Model):
    __tablename__ = "plugin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    def __repr__(self):
        return f"<Plugin {self.name}>"


class Hostel(db.Model):
    __tablename_ = "hostel"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    type = db.Column(db.String(64))
    rooms = db.relationship("HostelRoom", backref="hostel", lazy="dynamic")
    messages = db.relationship("HostelMessage", backref="hostel", lazy="dynamic")

    def __repr__(self):
        return f"<Hostel {self.name}>"


class HostelRoom(db.Model):
    __tablename = "hostel_room"
    id = db.Column(db.Integer, primary_key=True)
    hostel_id = db.Column(db.Integer, db.ForeignKey("hostel.id"))
    block = db.Column(db.String(32))
    level = db.Column(db.String(32))
    room = db.Column(db.String(32))
    users = db.relationship(
        "User", secondary=HostelRoomUserMap.__table__,
        backref=db.backref("hostel_rooms", lazy="dynamic"), lazy="dynamic"
    )

    def __repr__(self):
        return f"<HostelRoom {self.get_formatted_location()}>"

    def get_formatted_location(self):
        return f"{self.block}-{self.level}-{self.room}"

    def is_currently_available(self):
        return HostelRoomUserMap.query.filter(and_(
            HostelRoomUserMap.hostel_room_id == self.id,
            HostelRoomUserMap.academic_year == current_app.config["CURRENT_ACADEMIC_YEAR"],
            HostelRoomUserMap.semester == current_app.config["CURRENT_SEMESTER"]
        )).count() == 0


class HostelApplication(db.Model):
    __tablename_ = "hostel_application"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    hostel_id = db.Column(db.Integer, db.ForeignKey("hostel.id"))

    def __repr__(self):
        return f"<HostelApplication {self.id}>"


class HostelMessage(db.Model):
    __tablename_ = "hostel_message"
    id = db.Column(db.Integer, primary_key=True)
    hostel_id = db.Column(db.Integer, db.ForeignKey("hostel.id"))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(32))
    body = db.Column(db.String(1024))

    def __repr__(self):
        return f"<HostelMessage {self.title}>"
