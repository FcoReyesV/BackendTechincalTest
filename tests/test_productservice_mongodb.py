import unittest
from product.domain.product_model import Product
from product.application.product_service import ProductService
from product.application.anonymous_user_service import AnonymousUserService
from product.infrastructure.mongodb_product_repository import MongoDBProductRepository


class TestProductServiceWithMongodb(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(id="1", sku="Nik-US3-Lea-Bla", name="Nike Leather Black",
                                price=150.00, brand="Nike", anonymous_queries=5)
        self.product2 = Product(id="2", sku="Nik-US3-Lea-Whi", name="Nike Leather White",
                                price=160.00, brand="Nike", anonymous_queries=2)
        self.product2_update = Product(id="2", sku="Nik-US3-Lea-Whi", name="Nike Leather White",
                                       price=210.00, brand="Mike", anonymous_queries=2)
        self.db_mongorepository = MongoDBProductRepository("MONGO_URI")
        self.product_service = ProductService(self.db_mongorepository)
        self.anonymous_service = AnonymousUserService(self.db_mongorepository)

    def test_check_if_can_create_product_in_mongodb(self):
        # create the first admin
        self.product_service.create_product(self.product1)
        self.product_service.create_product(self.product2)

        # try to create a second admin with the same email
        result = self.product_service.create_product(self.product1)
        # check that the result is False (indicating that the admin was not created)
        self.assertEqual(result, False)

    def test_check_if_can_update_product_in_mongodb(self):
        self.product_service.update_product(self.product2_update)
        # Check if the admin's username and password were updated correctly
        updated_product = self.product_service.get_product_by_id(
            "sku", self.product2_update.sku)
        self.assertEqual(updated_product.brand, "Mike")
        self.assertEqual(updated_product.price, 210.00)

    def test_check_if_can_delete_product_in_mongo_db_by_id(self):
        self.product_service.delete_product("sku", self.product1.sku)

        deleted_product = self.product_service.get_product_by_id(
            "sku", self.product1.sku)
        self.assertEqual(deleted_product, None)

    def test_anonymous_user_queried_product_in_mongodb(self):
        try:
            product_to_query = self.product_service.get_product_by_id("sku", self.product2_update.sku)
            result_queried_product = self.anonymous_service.increment_anonymous_views(product_to_query)
            self.assertIsInstance(result_queried_product, Product)
        except Exception:
            self.assertEqual(product_to_query, None)

    def test_get_product_by_id_in_mongodb(self):
        result = self.product_service.get_product_by_id("sku", self.product2.sku)
        self.assertIsInstance(result, Product)