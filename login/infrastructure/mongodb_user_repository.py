from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv
from login.domain.user import User, user_schema
from login.application.user_repository import IUserRepository


class MongoDBUserRepository(IUserRepository):

    def __init__(self, mongo_uri: str) -> None:
        load_dotenv()
        self.__mongo_uri = getenv(mongo_uri)
        self.__client = MongoClient(self.__mongo_uri)
        self.__db = self.__client.database_admin_test
        self.__collection = self.__db.admins

    def get_user_by_email(self, email: str) -> User:
        result = self.__collection.find_one({"email": email})
        if result:
            return User(**result)
        else:
            return None
