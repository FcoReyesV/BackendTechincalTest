from product.application.product_repository import IProductRepository
from product.domain.product_model import Product

class ProductService:
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def create_product(self, new_product: Product) -> bool:
        if isinstance(self.get_product_by_id("sku", new_product.sku), Product):
            return False
        new_product.anonymous_queries = 0
        return self.__product_repository.create(new_product)

    def get_product_by_id(self, field: str, product_id: str) -> Product:
        product = self.__product_repository.get_by_id(field, product_id)
        return product if product else None

    def get_all_products(self) -> list[Product]:
        return self.__product_repository.get_all()

    def update_product(self, product: Product) -> bool:
        return self.__product_repository.update(product)

    def delete_product(self, field: str, product_id: str) -> bool:
        return self.__product_repository.delete(field, product_id)
