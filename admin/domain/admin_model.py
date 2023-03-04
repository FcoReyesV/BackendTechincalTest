from pydantic import BaseModel

class Admin(BaseModel):
    admin_id: str
    username: str
    email: str
    password: str
    is_superadmin: bool = False
    
    @classmethod
    def admin_schema(cls, admin) -> dict:
        return {"admin_id": str(admin["_id"]), "username": admin["username"],
                "email": admin["email"], "password": admin["password"], 
                "is_superadmin": admin["is_superadmin"]}

    @classmethod
    def admins_schema(cls, admins) -> list:
        return [cls.admin_schema(admin) for admin in admins]

class AdminNotFoundException(Exception):
    pass
