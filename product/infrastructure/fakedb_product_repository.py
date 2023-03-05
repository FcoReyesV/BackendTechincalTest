from product.domain.product_model import Product, increment_anonymous_queries
from product.application.product_repository import IProductRepository

product1 = Product(id="1", sku="Nik-US3-Lea-Bla", name="Nike Leather Black",
                   price=150.00, brand="Nike", anonymous_queries=5)
product2 = Product(id="2", sku="Nik-US3-Lea-Whi", name="Nike Leather White",
                   price=160.00, brand="Nike", anonymous_queries=2)
product3 = Product(id="3", sku="Nik-US3-Lea-Red", name="Nike Leather Red",
                   price=180.00, brand="Nike", anonymous_queries=0)

products_list = [product1, product2, product3]


class FakeDBProductRepository(IProductRepository):
    def create(self, new_product: Product) -> bool:
        products_list.append(new_product)
        return True

    def get_by_id(self, field: str, key) -> Product:
        for product_in_list in products_list:
            if product_in_list.sku == key:
                return product_in_list
        return None

    def get_all(self) -> list[Product]:
        return products_list

    def update(self, product: Product) -> bool:
        if not isinstance(self.get_by_id(None, product.sku), Product):
            return False
        for product_in_list in products_list:
            if product_in_list.sku == product.sku:
                product_in_list.sku = product.sku
                product_in_list.name = product.name
                product_in_list.price = product.price
                product_in_list.brand = product.brand
                product_in_list.anonymous_queries = product_in_list.anonymous_queries
                return True
        return False

    def delete(self, field: str, key) -> bool:
        product_to_delete = self.get_by_id(field, key)
        if not isinstance(product_to_delete, Product):
            return False
        for i, product_in_list in enumerate(products_list):
            if product_to_delete == product_in_list:
                del products_list[i]
                return True
        return False
    
    def increment_anonymous_views(self, product: Product) -> Product:
        for i, product_in_list in enumerate(products_list):
            if product == product_in_list:
                product_in_list.anonymous_queries = increment_anonymous_queries(product_in_list.anonymous_queries)
                return product_in_list
        return None
