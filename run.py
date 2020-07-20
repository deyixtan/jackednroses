from webapp import create_app, db
from webapp.models import User, UserProfile, Module, ModuleAnnouncement, ModuleTask, Plugin, UHMSMessage
app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "UserProfile": UserProfile,
        "Module": Module,
        "ModuleAnnouncement": ModuleAnnouncement,
        "ModuleTask": ModuleTask,
        "Plugin": Plugin,
        "UHMSMessage": UHMSMessage
    }
