import abc
from typing import Optional
from product.domain.product_model import Product


class IProductRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, new_product: Product) -> bool:
        pass
    
    @abc.abstractmethod
    def get_by_id(self, field: str, key: str) -> Optional[Product]:
        pass

    @abc.abstractmethod
    def get_all(self) -> list[Product]:
        pass

    @abc.abstractmethod
    def update(self, product: Product) -> bool:
        pass

    @abc.abstractmethod
    def delete(self, field: str, key: str) -> bool:
        pass

    @abc.abstractmethod
    def increment_anonymous_views(self, product: Product) -> Product:
        pass
