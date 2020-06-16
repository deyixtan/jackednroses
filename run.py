# run.py
from webapp import create_app, db
from webapp.models import User, Module, Enrolled

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Module": Module,
        "Enrolled": Enrolled
    }

# Python script entry point
if __name__ == "__main__":
    app.run(debug=True)
