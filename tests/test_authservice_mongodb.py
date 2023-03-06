import unittest
from login.domain.user import User
from login.infrastructure.auth_service import AuthService
from login.infrastructure.mongodb_user_repository import MongoDBUserRepository

admin1 = User(email="lmethod1234@gmail.com",
              password="$2a$12$3RxMb1gEKXn3J5sKe1YZI.s8lHrGBlYREs.tye.Uz.ARZJ1wdFSI2")
admin2 = User(email="picko.gamess@gmail.com",
              password="$2a$12$3RxMb1gEKXn3J5sKe1YZI.s8lHrGBlYREs.tye.Uz.ARZJ1wdFSI2")
class TestLoginService(unittest.TestCase):
    def setUp(self):
        self.mongodb_repo = MongoDBUserRepository("MONGO_URI")

    def test_check_if_mongodb_repo_is_returning_a_user_with_same_email(self):
        try:
            user_in_db = self.mongodb_repo.get_user_by_email(
            admin2.email)
            self.assertEqual(user_in_db.email, admin2.email)
            self.assertEqual(user_in_db.password, admin2.password)
        except Exception:
            self.assertEqual(user_in_db, None)
