from login.domain.user import User
from login.application.user_repository import IUserRepository

admin1 = User(email="lmethod1234@gmail.com", password="1234")
admin2 = User(email="lmethod@gmail.com", password="1234")
admin3 = User(email="picko13@gmail.com@gmail.com", password="1234")

user_list = [admin1, admin2, admin3]


class FakeDBUserRepository(IUserRepository):
    def get_user_by_email(self, email: str) -> User:
        for user_in_list in user_list:
            if user_in_list.email == email:
                return user_in_list
        return None
