import unittest
from admin.domain.admin_model import Admin
from admin.application.admin_service import AdminService
from admin.infrastructure.mongodb_admin_repository import MongoDBSuperAdminRepository

class TestAdminServiceWithMongodb(unittest.TestCase):
    def setUp(self):
        self.admin1 = Admin(admin_id="5", username="picko",
                            email="picko1@gmail.com", password="123", is_superadmin=False)
        self.admin2 = Admin(admin_id="4", username="picko3",
                            email="picko13@gmail.com", password="234", is_superadmin=False)
        self.admin2_update = Admin(admin_id="", username="packo_1",
                                email="picko13@gmail.com", password="321", is_superadmin=False)
        self.admin_service = AdminService(MongoDBSuperAdminRepository("MONGO_URI"))

    def test_check_if_can_create_admin_in_mongodb(self):
        # create the first admin
        self.admin_service.create_admin(self.admin1)
        self.admin_service.create_admin(self.admin2)

        # try to create a second admin with the same email
        result = self.admin_service.create_admin(self.admin1)
        # check that the result is False (indicating that the admin was not created)
        self.assertEqual(result, False)
            
    def test_check_if_can_update_admin_in_mongodb(self):
        self.admin_service.update_admin(self.admin2_update)
        # Check if the admin's username and password were updated correctly
        updated_admin = self.admin_service.get_admin_by_id(
            "email", self.admin2_update.email)
        self.assertEqual(updated_admin.username, "packo_1")
        self.assertEqual(updated_admin.password, "321")    
    
    def test_check_if_can_delete_admin_in_mongo_db_by_id(self):
        self.admin_service.delete_admin("email", self.admin1.email)

        deleted_admin = self.admin_service.get_admin_by_id(
            "email",self.admin1.email)
        self.assertEqual(deleted_admin, None)
