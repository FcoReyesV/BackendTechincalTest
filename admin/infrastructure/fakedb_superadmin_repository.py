from admin.domain.admin_model import Admin
from admin.application.superadmin_repository import ISuperAdminRepository

admin1 = Admin(admin_id= "1",username= "PacoAdmin",
                     email= "lmethod1234@gmail.com",password= "1234", is_superadmin=False)
admin2 = Admin(admin_id= "2", username= "Paco4Admin",
                     email= "lmethod@gmail.com", password= "1234", is_superadmin=False)
admin3 = Admin(admin_id= "3", username= "Paco3Admin",
                     email= "1234@gmail.com", password= "1234", is_superadmin=False)

admin_list = [admin1, admin2, admin3]

class FakeDBSuperAdminRepository(ISuperAdminRepository):
    def create(self, new_admin: Admin) -> bool:
        admin_list.append(new_admin)
        return True
    
    def get_by_id(self, field: str, key) -> Admin:
        for admin_in_list in admin_list:
            if admin_in_list.email == key:
                return admin_in_list
        return None
    
    def get_all(self) -> list[Admin]:
        return admin_list
    
    def update(self, admin_to_update: Admin) -> bool:
        if not isinstance(self.get_by_id(None, admin_to_update.email), Admin):
            return False
        for admin_in_list in admin_list:
            if admin_in_list.email == admin_to_update.email:
                admin_in_list.username = admin_to_update.username
                admin_in_list.email = admin_to_update.email
                admin_in_list.password = admin_to_update.password
                return True
        return False
    
    def delete(self, field: str, key) -> bool:
        admin_to_delete = self.get_by_id(field, key)
        if not isinstance(admin_to_delete, Admin):
            return False
        for i, admin_in_list in enumerate(admin_list):
            if admin_to_delete == admin_in_list:
                del admin_list[i]
                return True
        return False
    
