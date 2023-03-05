from product.application.product_repository import IProductRepository
from product.domain.product_model import Product

class AnonymousUserService:
    def __init__(self, product_repository:  IProductRepository):
        self.__product_repository = product_repository

    def increment_anonymous_views(self, product: Product) -> Product:
        return self.__product_repository.increment_anonymous_views(product)
