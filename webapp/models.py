from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from webapp import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Association Tables
module_user_map = db.Table(
    "module_user_map",
    db.Column("module_id", db.Integer, db.ForeignKey("module.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

module_plugin_map = db.Table(
    "module_plugin_map",
    db.Column("module_id", db.Integer, db.ForeignKey("module.id")),
    db.Column("plugin_id", db.Integer, db.ForeignKey("plugin.id"))
)

module_task_user_map = db.Table(
    "module_task_user_map",
    db.Column("task_id", db.Integer, db.ForeignKey("module_task.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("info", db.String(1024))
)


# Object Tables
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    profile = db.relationship("UserProfile", backref="user", lazy="dynamic")
    modules = db.relationship(
        "Module", secondary=module_user_map,
        primaryjoin="module_user_map.c.module_id == Module.id",
        secondaryjoin="module_user_map.c.user_id == User.id",
        backref=db.backref("users", lazy="dynamic"), lazy="dynamic"
    )
    tasks = db.relationship(
        "ModuleTask", secondary=module_task_user_map,
        primaryjoin="module_task_user_map.c.task_id == ModuleTask.id",
        secondaryjoin="module_task_user_map.c.user_id == User.id",
        backref=db.backref("users", lazy="dynamic"), lazy="dynamic"
    )

    def __repr__(self):
        return "<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserProfile(db.Model):
    __tablename__ = "user_profile"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    nric = db.Column(db.String(16), index=True, unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    gender = db.Column(db.String(16))
    birth_date = db.Column(db.DateTime)
    marital_status = db.Column(db.String(16))
    nationality = db.Column(db.String(32))
    mobile_number = db.Column(db.Integer)
    home_number = db.Column(db.Integer)
    home_address = db.Column(db.String(128))
    emergency_contact_name = db.Column(db.String(64))
    emergency_contact_number = db.Column(db.Integer)

    def __repr__(self):
        return "<UserProfile {self.get_full_name}>"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Module(db.Model):
    __tablename__ = "module"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64))
    academic_year = db.Column(db.String(16))
    semester = db.Column(db.Integer)
    announcements = db.relationship("ModuleAnnouncement", backref="module", lazy="dynamic")
    tasks = db.relationship("ModuleTask", backref="module", lazy="dynamic")
    plugins = db.relationship(
        "Plugin", secondary=module_plugin_map,
        primaryjoin="module_plugin_map.c.module_id == Module.id",
        secondaryjoin="module_plugin_map.c.plugin_id == Plugin.id",
        backref=db.backref("modules", lazy="dynamic"), lazy="dynamic"
    )

    def __repr__(self):
        return f"<Module {self.code}>"

    def enable_plugin(self, plugin):
        if not self.is_plugin_enabled(plugin):
            self.plugins.append(plugin)
            db.session.commit()

    def disable_plugin(self, plugin):
        if self.is_plugin_enabled(plugin):
            self.plugins.remove(plugin)
            db.session.commit()

    def is_plugin_enabled(self, plugin):
        return self.plugins.filter(module_plugin_map.c.plugin_id == plugin.id).count() > 0


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
    timestamp = db.Column(db.DateTime)
    location = db.Column(db.String(32))

    def __repr__(self):
        return f"<ModuleTask {self.title}>"


class Plugin(db.Model):
    __tablename__ = "plugin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    def __repr__(self):
        return f"<Plugin {self.name}>"


class UHMSMessage(db.Model):
    __tablename_ = "uhms_message"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(32))
    body = db.Column(db.String(1024))

    def __repr__(self):
        return f"<UHMSMessage {self.title}>"
