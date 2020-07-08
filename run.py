# run.py
from webapp import create_app, db
from webapp.models import User, Module, Enrolled, UserDetails

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Module": Module,
        "Enrolled": Enrolled,
        "UserDetails": UserDetails
    }
