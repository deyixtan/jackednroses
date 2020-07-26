import unittest
from datetime import datetime, timedelta
from webapp import create_app, db
from webapp.models import ModuleUserMap, ModulePluginMap, ModuleTaskUserMap, HostelRoomUserMap, User, UserProfile, Module, ModuleAnnouncement, ModuleTask, Plugin, Hostel, HostelRoom, HostelApplication, HostelMessage
from config import Config
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError


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
    
    #user related tests
    def test_password_hashing(self):
        u = User(username="E1234567")
        u.set_password("warmthecockles")
        self.assertFalse(u.check_password("titanicSinking"))
        self.assertTrue(u.check_password("warmthecockles"))

    def test_user_integrity_check(self):
        u = User(username="E1234567")
        db.session.add(u)
        db.session.commit()
        u2 = User(username="E1234567")
        with self.assertRaises(Exception) as context:
            db.session.add(u2)
            db.session.commit()
        self.assertEqual(type(context.exception), IntegrityError)

    def test_userprofile_creation(self):
        u = User(username="E1234567")
        db.session.add(u)
        db.session.commit()
        ud = UserProfile(user_id=u.id, nric="S1234567A", mobile_number=91234567)
        db.session.add(ud)
        db.session.commit()
        self.assertEqual(UserProfile.query.filter_by(user_id=u.id).first(), ud)

    def test_userprofile_update(self):
        u = User(username="E1234567")
        db.session.add(u)
        db.session.commit()
        ud = UserProfile(user_id=u.id, nric="S1234567A", first_name="Billy", last_name="Eyelash", gender="Male", marital_status="Single", nationality="Singaporean", mobile_number=91234567, home_number=61234567, home_address="Orchard Road Block 123 #01-01", emergency_contact_name="Gill Bates", emergency_contact_number=81234567)
        db.session.add(ud)
        db.session.commit()
        ud.first_name = "Billie"
        ud.last_name = "Eilish"
        ud.gender = "Female"
        ud.marital_status = "Married"
        ud.nationality = "Russian"
        ud.mobile_number = 97654321
        ud.home_number = 67654321
        ud.home_address = "Tuas Checkpoint #01-02"
        ud.emergency_contact_name = "Melon Musk"
        ud.emergency_contact_number = 87654321
        db.session.add(ud)
        db.session.commit()
        self.assertEqual(UserProfile.query.filter_by(user_id=u.id).first(), ud)

    #module related tests
    def test_module_creation_and_enrolllment(self):
        m = Module(code="CS2100", academic_year=2019, semester=1)
        u = User(username="E1234567")
        db.session.add(m)
        db.session.add(u)
        db.session.commit()
        e = ModuleUserMap(module_id=m.id, user_id=u.id)
        db.session.add(e)
        db.session.commit()
        self.assertEqual(Module.query.filter_by(code="CS2100", academic_year=2019, semester=1).first(), m)
        self.assertEqual(ModuleUserMap.query.filter_by(user_id=u.id, module_id=m.id).first(), e)

    def test_module_integrity_check(self):
        m = Module(code="CS2100", academic_year=2019, semester=1)
        db.session.add(m)
        db.session.commit()
        m2 = Module(code="CS2100", academic_year=2019, semester=1)
        self.assertEqual(m2.check_exist(m2), m)

    def test_enrollment_integrity_check(self):
        m = Module(code="CS2100", academic_year=2019, semester="1")
        u = User(username="E1234567")
        db.session.add(m)
        db.session.add(u)
        db.session.commit()
        e = ModuleUserMap(module_id=m.id, user_id=u.id)
        db.session.add(e)
        db.session.commit()
        e2 = ModuleUserMap(module_id=m.id, user_id=u.id)
        with self.assertRaises(Exception) as context:
            db.session.add(e2)
            db.session.commit()
        self.assertEqual(type(context.exception), FlushError)
    
    def test_announcement_creation(self):
        m = Module(code="CS2100", academic_year=2019, semester=1)
        db.session.add(m)
        db.session.commit()
        a = ModuleAnnouncement(module_id=m.id, title="Announcement Title")
        db.session.add(a)
        db.session.commit()
        self.assertEqual(ModuleAnnouncement.query.filter_by(module_id=m.id, title=a.title).first(), a)

    def test_task_creation(self):
        m = Module(code="CS2100", academic_year=2019, semester=1)
        db.session.add(m)
        db.session.commit()
        t = ModuleTask(module_id=m.id, title="Task Title")
        db.session.add(t)
        db.session.commit()
        self.assertEqual(ModuleTask.query.filter_by(module_id=m.id).first(), t)

    #hostel tests
    def test_hostel_and_room_creation(self):
        h = Hostel(name="Stardew Valley Hall", type="Hall")
        h2 = Hostel(name="Harvest Moon Hall", type="Hall")
        db.session.add(h)
        db.session.add(h2)
        db.session.commit()
        r = HostelRoom(hostel_id=h.id, block="1")
        r2 = HostelRoom(hostel_id=h2.id, block="1A")
        db.session.add(r)
        db.session.add(r2)
        db.session.commit()
        self.assertEqual(HostelRoom.query.filter_by(hostel_id=h.id, block=r.block).first(), r)
        self.assertEqual(HostelRoom.query.filter_by(hostel_id=h2.id, block=r2.block).first(), r2)

    def hostel_approval_and_message_check(self):
        h = Hostel(name="Stardew Valley Hall", type="Hall")
        r = HostelRoom(hostel_id=h.id, block="1")
        msg = HostelMessage(hostel_id=h.id, title="Welcome to Stardew Valley!")
        u = User(username="E1234567")
        db.session.add(h)
        db.session.add(r)
        db.session.add(hmsg)
        db.session.add(u)
        db.session.commit()
        happ = HostelApplication(user_id=u.id, hostel_id=h.id)
        db.session.add(ha)
        db.session.commit()
        hmap = HostelRoomUserMap(hostel_room_id=r.id, user_id=happ.id)
        db.session.add(hmap)
        db.session.commit()
        self.assertEqual(User.query.filter_by(user_id=u.id).first().hostel_room.hostel.messages, msg)
        
if __name__ == "__main__":
    unittest.main(verbosity=2)
