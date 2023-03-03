import abc
from admin.domain import admin, superadmin_repository

class AdminController():
    
    def __init__(self, superadmin_repository: superadmin_repository.ISuperAdminRepository) -> None:
        self.superadmin_repository = superadmin_repository

    def create_admin(self, admin: admin.Admin):
        self.superadmin_repository.create_admin(admin)

    def update_admin(self, admin: admin.Admin):
        self.superadmin_repository.update_admin(admin)

    def delete_admin(self, id: str):
        self.superadmin_repository.delete_admin(id)
