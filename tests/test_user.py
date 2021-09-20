import unittest
from app.models import User
from app.commands import db


class UserTest(unittest.TestCase):
    """
    test class for the User Model
    """
    def setUp(self):
        self.new_user = User(username='zoo-test', password='password1234', email='tests@example.com')

    def tearDown(self) -> None:
        self.new_user = None

    def test_password_setter(self):
        self.assertTrue(self.new_user.secure_password is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('password1234'))

    def test_user_exists(self):
        self.assertEqual(self.new_user.username, 'zoo-test')
        self.assertEqual(self.new_user.email, 'tests@example.com')

    def test_user_save(self):
        self.new_user.save_user()
        username = self.new_user.username
        query = db.session.query(User).filter_by(username=username).first()
        self.assertEqual(self.new_user.username, query.username)
        self.new_user.delete()

    def test_user_delete(self):
        self.new_user.save_user()
        self.new_user.delete()
