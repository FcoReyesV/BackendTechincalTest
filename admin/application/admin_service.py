from admin.application.superadmin_repository import ISuperAdminRepository
from admin.domain.admin_model import Admin

class AdminService:
    def __init__(self, admin_repository: ISuperAdminRepository):
        self.__admin_repository = admin_repository

    def create_admin(self, new_admin: Admin) -> bool:
        if isinstance(self.get_admin_by_id("email", new_admin.email), Admin):
            return False
        return self.__admin_repository.create(new_admin)
    
    def get_admin_by_id(self, field: str, admin_id: str) -> Admin:
        admin = self.__admin_repository.get_by_id(field, admin_id)
        return admin if admin else None
    
    def get_all_admins(self) -> list[Admin]:
        return self.__admin_repository.get_all()
    
    def update_admin(self, admin: Admin) -> bool:
        admin.is_superadmin = False
        return self.__admin_repository.update(admin)
    
    def delete_admin(self, field: str, admin_id: str) -> bool:
        return self.__admin_repository.delete(field, admin_id)

