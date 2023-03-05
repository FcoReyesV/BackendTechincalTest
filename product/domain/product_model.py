from pydantic import BaseModel

class Product(BaseModel):
    id: str
    sku: str
    name: str
    price: float
    brand: str
    anonymous_queries: int

def increment_anonymous_queries(anonymous_queries) -> int:
    return anonymous_queries + 1

def product_schema(product) -> dict:
    return {"id": str(product["_id"]), "sku": product["sku"],
            "name": product["name"], "price": product["price"],
            "brand": product["brand"], "anonymous_queries": product["anonymous_queries"]}

def products_schema(products) -> list:
    return [product_schema(product) for product in products]
