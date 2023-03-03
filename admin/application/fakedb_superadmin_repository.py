from admin.domain import admin, superadmin_repository

admin1 = admin.Admin(admin_id= "1",username= "PacoAdmin", 
                     email= "lmethod1234@gmail.com",password= "1234")
admin2 = admin.Admin(admin_id= "2", username= "Paco4Admin",
                     email= "lmethod@gmail.com", password= "1234")
admin3 = admin.Admin(admin_id= "3", username= "Paco3Admin",
                     email= "1234@gmail.com", password= "1234")

admin_list = [admin1, admin2, admin3]

class FakeDBSuperAdminRepository(superadmin_repository.ISuperAdminRepository):

    def get_admin(self, id_admin: str) -> admin.Admin:
        admin_found = None
        for admin_in_list in admin_list:
            if admin_in_list.admin_id == id_admin:
                admin_found = admin_in_list
                break
        return admin_found
    
    def get_all_admins(self) -> list[admin.Admin]:
        return admin_list
    
    def create_admin(self, new_admin: admin.Admin) -> admin.Admin:
        if type(self.get_admin(new_admin)) == admin.Admin:
            return None
        admin_list.append(new_admin)
        return admin_list
    
    def update_admin(self, admin_to_update: admin.Admin) -> admin.Admin:
        if type(self.get_admin(admin_to_update)) == admin.Admin:
            return None
        for admin_in_list in admin_list:
            if admin_in_list.admin_id == admin_to_update:
                admin_in_list = admin_to_update
                return admin_in_list
    
    def delete_admin(self, id_admin: str) -> None:
        admin_to_delete = self.get_admin(id_admin)
        if type(admin_to_delete) == admin.Admin:
            for i, admin_in_list in enumerate(admin_list):
                if admin_to_delete == admin_in_list:
                    del admin_in_list[i]
                    return None
        return {"error": "could not delete admin"}
    
