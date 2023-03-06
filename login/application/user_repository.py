import abc
from login.domain.user import User

class IUserRepository(abc.ABC):
    @abc.abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass
