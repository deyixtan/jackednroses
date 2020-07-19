from webapp import create_app, db
from webapp.models import Announcement, Enrolled, Exam, ExamDetails, Module, Task, User, UserDetails

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Announcement": Announcement,
        "Enrolled": Enrolled,
        "Exam": Exam,
        "ExamDetails": ExamDetails,
        "Module": Module,
        "Task": Task,
        "User": User,
        "UserDetails": UserDetails
    }
