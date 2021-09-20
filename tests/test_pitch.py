import unittest
from app.models import UserPitch
from app.commands import db


class UserPitchTest(unittest.TestCase):
    """
    test class for the User Pitch Model
    """

    def setUp(self):
        self.new_pitch = UserPitch(title="test", pitch="simple pitch", user_id=3, category="Idea")

    def tearDown(self) -> None:
        self.new_pitch = None

    def test_pitch_exists(self):
        self.assertEqual(self.new_pitch.title, "test")
        self.assertEqual(self.new_pitch.pitch, "simple pitch")
        self.assertEqual(self.new_pitch.user_id, 3)

    def test_user_save(self):
        self.new_pitch.save_pitch()
        title = self.new_pitch.title

        query = db.session.query(UserPitch).filter_by(title=title).first()
        self.assertEqual(self.new_pitch.title, query.title)
        self.new_pitch.delete_pitch()

    def test_user_delete(self):
        self.new_pitch.save_pitch()
        self.new_pitch.delete_pitch()
