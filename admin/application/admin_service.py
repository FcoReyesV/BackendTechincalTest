from admin.application.superadmin_repository import ISuperAdminRepository, AdminRepositoryException
from admin.domain.admin_model import Admin

class AdminService:
    def __init__(self, admin_repository: ISuperAdminRepository):
        self.__admin_repository = admin_repository

    def create_admin(self, new_admin: Admin) -> AdminRepositoryException | bool:
        if isinstance(self.get_admin_by_id("email", new_admin.email), Admin):
            raise AdminRepositoryException(f"Admin with id {new_admin.email} already in db")
        result = self.__admin_repository.create(new_admin)
        if result:
            return result
        raise AdminRepositoryException("Admin could not be created in db")
    
    def get_admin_by_id(self, field: str, admin_id: str) -> Admin:
        admin = self.__admin_repository.get_by_id(field, admin_id)
        return admin if admin else None
    
    def get_all_admins(self) -> list[Admin]:
        return self.__admin_repository.get_all()
    
    def update_admin(self, admin: Admin) -> bool:
        # If the admin already has the values we are trying to update, we return True directly
        current_admin = self.get_admin_by_id("email", admin.email)
        if (current_admin is not None and current_admin.username == admin.username and
            current_admin.password == admin.password):
            raise AdminRepositoryException(f"Admin with id {current_admin.email} already updated")
        admin.is_superadmin = False
        result = self.__admin_repository.update(admin)
        if result:
            return result
        raise AdminRepositoryException(
            f"Admin with id {current_admin.email} could not be updated")
    
    def delete_admin(self, field: str, admin_id: str) -> bool:
        result = self.__admin_repository.delete(field, admin_id)
        if result:
            return result
        raise AdminRepositoryException(
            f"Admin with {field} {admin_id} not found")

