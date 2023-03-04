from admin.application.superadmin_repository import ISuperAdminRepository, AdminRepositoryException
from admin.domain.admin_model import Admin

class AdminService:
    def __init__(self, admin_repository: ISuperAdminRepository):
        self.__admin_repository = admin_repository

    def create_admin(self, new_admin: Admin) -> Admin:
        result = self.__admin_repository.create(new_admin)
        if result:
            return new_admin
        raise AdminRepositoryException("Admin could not be created in db")
    
    def get_admin_by_id(self, field: str, admin_id: str) -> Admin:
        admin = self.__admin_repository.get_by_id(field, admin_id)
        if admin:
            return admin
        raise AdminRepositoryException(f"Admin with id {admin_id} not found")
    
    def get_all_admins(self) -> list[Admin]:
        return self.__admin_repository.get_all()
    
    def update_admin(self, admin: Admin) -> Admin:
        admin.is_superadmin = False
        result = self.__admin_repository.update(admin)
        if result:
            return admin
        raise AdminRepositoryException(f"Admin with mail {admin.email} not found")
    
    def delete_admin(self, field: str, admin_id: str) -> bool:
        result = self.__admin_repository.delete(field, admin_id)
        if result:
            return True
        raise AdminRepositoryException(f"Admin with {field} {admin_id} not found")

