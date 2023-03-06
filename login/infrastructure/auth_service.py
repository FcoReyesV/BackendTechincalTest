from os import getenv
from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from login.application.user_repository import IUserRepository
from login.domain.user import User, Token

crypt = CryptContext(schemes=["bcrypt"])

class AuthService:
    def __init__(self, user_repository: IUserRepository):
        load_dotenv()
        self.__user_repository = user_repository
        self.__secret_key = getenv("SECRET_KEY_JWT_LOGIN")
        self.__algorithm = getenv("ALGORITHM_JWT_LOGIN")
        self.__access_token_expire_minutes = 30

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.__user_repository.get_user_by_email(email)
        if not isinstance(user, User):
            return None
        if not crypt.verify(password, user.password):
            return None
        return user

    def create_access_token(self, user: User) -> Token:
        expires_delta = timedelta(minutes=self.__access_token_expire_minutes)
        expires_at = datetime.utcnow() + expires_delta
        to_encode = {"sub": user.email, "exp": expires_at}
        encoded_jwt = jwt.encode(
            to_encode, self.__secret_key, algorithm=self.__algorithm)
        return Token(access_token=encoded_jwt, token_type="bearer")

    def get_email_by_token(self, token: str) -> str:
        if not token:
            return None
        decoded_token = jwt.decode(
            token, self.__secret_key, algorithms=[self.__algorithm])
        return decoded_token.get("sub")
