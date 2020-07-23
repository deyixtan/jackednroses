from webapp import create_app, db
from webapp.models import Hostel, HostelApplication, HostelMessage, HostelRoom, HostelRoomUserMap, User, UserProfile, Module, ModuleAnnouncement, ModuleTask, Plugin

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Hostel": Hostel,
        "HostelApplication": HostelApplication,
        "HostelMessage": HostelMessage,
        "HostelRoom": HostelRoom,
        "HostelRoomUserMap": HostelRoomUserMap,
        "User": User,
        "UserProfile": UserProfile,
        "Module": Module,
        "ModuleAnnouncement": ModuleAnnouncement,
        "ModuleTask": ModuleTask,
        "Plugin": Plugin,
    }
