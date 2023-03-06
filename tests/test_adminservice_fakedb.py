import unittest
from admin.domain.admin_model import Admin
from admin.application.admin_service import AdminService
from admin.infrastructure.fakedb_superadmin_repository import FakeDBSuperAdminRepository

class TestAdminService(unittest.TestCase):
    def setUp(self):
        self.admin1 = Admin(admin_id="5", username="picko", 
                            email="picko1@gmail.com", password="123",is_superadmin=False)
        self.admin2 = Admin(admin_id="4", username="picko3",
                            email="picko13@gmail.com", password="234",is_superadmin=False)
        self.admin3_update = Admin(admin_id="3", username="francisco",
                                   email="1234@gmail.com", password="123paco", is_superadmin=False)
        self.admin_service = AdminService(FakeDBSuperAdminRepository())
    
    def test_create_admin_in_fake_db(self):
        # create the first admin
        self.admin_service.create_admin(self.admin1)
        self.admin_service.create_admin(self.admin2)

        # try to create a second product with the same sku
        result = self.admin_service.create_admin(self.admin1)
        # check that the result is False (indicating that the admin was not created)
        self.assertEqual(result, False)

    def test_update_admin_in_fake_db(self) -> None:
        self.admin_service.update_admin(self.admin3_update)
        # Check if the admin's username and password were updated correctly
        updated_admin = self.admin_service.get_admin_by_id(
            "email", self.admin3_update.email)
        self.assertEqual(updated_admin.username, "francisco")
        self.assertEqual(updated_admin.password, "123paco")

    def test_delete_admin_in_fake_db(self) -> None:
        self.admin_service.delete_admin("email", self.admin1.email)
        deleted_admin = self.admin_service.get_admin_by_id(
            "email", self.admin1.email)
        self.assertEqual(deleted_admin, None)