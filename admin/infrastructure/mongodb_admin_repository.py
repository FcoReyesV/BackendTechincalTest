from os import getenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from admin.domain.admin_model import Admin
from admin.application.superadmin_repository import ISuperAdminRepository

class MongoDBSuperAdminRepository(ISuperAdminRepository):

    def __init__(self, mongo_uri: str) -> None:
        load_dotenv()
        self.__mongo_uri = getenv(mongo_uri)
        self.__client = MongoClient(self.__mongo_uri)
        self.__db = self.__client.database_admin_test
        self.__collection = self.__db.admins

    def create(self, new_admin: Admin) -> bool:
        admin_dict = vars(new_admin)
        admin_dict.pop("admin_id", None)
        result = self.__collection.insert_one(admin_dict)
        return bool(result.inserted_id)
    
    def get_by_id(self, field: str, key) -> Admin:
        result = self.__collection.find_one({field: ObjectId(key)})
        if result:
            return Admin.admin_schema(result)
        return None

    def get_all(self) -> list[Admin]:
        results = self.__collection.find()
        if results:
            return [Admin(**admin) for admin in Admin.admins_schema(results)]
        return []
    
    def update(self, admin_to_update: Admin) -> bool:
        admin_dict = vars(admin_to_update)
        admin_dict.pop("admin_id", None)
        result = self.__collection.find_one_and_update(
            {"_id": ObjectId(admin_to_update.admin_id)}, admin_dict)
        return bool(result.modified_count)

    def delete(self, field: str, key) -> bool:
        result = self.__collection.delete_one({field: key})
        return bool(result.deleted_count)
