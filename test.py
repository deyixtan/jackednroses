import unittest
from datetime import datetime, timedelta
from webapp import create_app, db
from webapp.models import User, Module, Enrolled, Announcement, Task, Exam, ExamDetails, UserDetails, UhmsMessages
from config import Config
from sqlalchemy.exc import IntegrityError


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(nusnetid="E1234567")
        u.set_password("warmthecockles")
        self.assertFalse(u.check_password("titanicSinking"))
        self.assertTrue(u.check_password("warmthecockles"))

    def test_module_creation_and_enrolllment(self):
        m = Module(code="CS2100", academic_year="2019/2020", semester=1)
        db.session.add(m)
        db.session.commit()
        u = User(nusnetid="E1234567")
        e = Enrolled(nusnetid=u.nusnetid)
        e.set_module(code=m.code, academic_year=m.academic_year, semester=m.semester)
        db.session.add(u)
        db.session.add(e)
        db.session.commit()
        self.assertEqual(m.check_exist(m), m)
        self.assertEqual(Enrolled.query.filter_by(nusnetid=u.nusnetid, module_id=m.id).first(), e)

    def test_announcement_creation(self):
        m = Module(code="CS2100", academic_year="2019/2020", semester=1)
        db.session.add(m)
        db.session.commit()
        a = Announcement(module_id=m.id, title="Announcement Title")
        db.session.add(a)
        db.session.commit()
        self.assertEqual(Announcement.query.filter_by(module_id=m.id, title=a.title).first(), a)

    def test_task_creation(self):
        m = Module(code="CS2100", academic_year="2019/2020", semester=1)
        db.session.add(m)
        db.session.commit()
        t = Task(module_id=m.id, taskname="Task Title")
        db.session.add(t)
        db.session.commit()
        self.assertEqual(Task.query.filter_by(module_id=m.id).first(), t)

    def test_exam_creation(self):
        m = Module(code="CS2100", academic_year="2019/2020", semester="1")
        u = User(nusnetid="E1234567")
        db.session.add(m)
        db.session.add(u)
        db.session.commit()
        e = Exam(module_id=m.id, examname="Exam Name")
        db.session.add(e)
        db.session.commit()
        ed = ExamDetails(nusnetid=u.nusnetid, exam_id=e.id)
        db.session.add(ed)
        db.session.commit()
        self.assertEqual(Exam.query.filter_by(module_id=m.id).first(), e)
        self.assertEqual(ExamDetails.query.filter_by(nusnetid=u.nusnetid, exam_id=e.id).first(), ed)

    def test_userdetails_creation(self):
        u = User(nusnetid="E1234567")
        db.session.add(u)
        db.session.commit()
        ud = UserDetails(nusnetid=u.nusnetid, nric="S1234567A", mobilenum=91234567)
        db.session.add(ud)
        db.session.commit()
        self.assertEqual(UserDetails.query.filter_by(nusnetid=u.nusnetid).first().nusnetid, u.nusnetid)

    def test_userdetails_update(self):
        u = User(nusnetid="E1234567")
        db.session.add(u)
        db.session.commit()
        ud = UserDetails(nusnetid=u.nusnetid, nric="S1234567A", gender="Male", marital_status="Single", nationality="Singaporean", mobilenum=91234567, homenum=61234567, address="Orchard Road Block 123 #01-01", emergencycontactname="Gill Bates", emergencycontactnum=81234567)
        db.session.add(ud)
        db.session.commit()
        ud.nric = "S7654321B"
        ud.gender = "Female"
        ud.marital_status = "Married"
        ud.nationality = "Australian"
        ud.mobilenum = 97654321
        ud.homenum = 67654321
        ud.address = "Tuas Checkpoint #01-02"
        ud.emergencycontactname = "Melon Musk"
        ud.emergencycontactnum = 87654321
        db.session.add(ud)
        db.session.commit()
        self.assertEqual(UserDetails.query.filter_by(nusnetid=u.nusnetid).first(), ud)

    def test_user_integrity_check(self):
        u = User(nusnetid="E1234567")
        db.session.add(u)
        db.session.commit()
        u2 = User(nusnetid="E1234567")
        with self.assertRaises(Exception) as context:
            db.session.add(u2)
            db.session.commit()
        self.assertEqual(type(context.exception), IntegrityError)

    def test_module_integrity_check(self):
        m = Module(code="CS2100", academic_year="2019/2020", semester=1)
        db.session.add(m)
        db.session.commit()
        m2 = Module(code="CS2100", academic_year="2019/2020", semester=1)
        self.assertEqual(m2.check_exist(m2), m)

if __name__ == "__main__":
    unittest.main(verbosity=2)
