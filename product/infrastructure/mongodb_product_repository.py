from os import getenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from product.domain.product_model import Product, product_schema, products_schema, increment_anonymous_queries
from product.application.product_repository import IProductRepository


class MongoDBProductRepository(IProductRepository):

    def __init__(self, mongo_uri: str) -> None:
        load_dotenv()
        self.__mongo_uri = getenv(mongo_uri)
        self.__client = MongoClient(self.__mongo_uri)
        self.__db = self.__client.database_product_test
        self.__collection = self.__db.products

    def create(self, new_product: Product) -> bool:
        product_dict = vars(new_product)
        product_dict.pop("id", None)
        result = self.__collection.insert_one(product_dict)
        return bool(result.inserted_id)

    def get_by_id(self, field: str, key) -> Product:
        result = self.__collection.find_one({field: key})
        if result:
            product_dict = product_schema(result)
            return Product(**product_dict)
        return None

    def get_all(self) -> list[Product]:
        results = products_schema(self.__collection.find())
        if results:
            return [Product(**product) for product in results]
        return []

    def update(self, product: Product) -> bool:
        product_dict = vars(product)
        product_dict.pop("id")
        update_dict = {"$set": product_dict}
        result = self.__collection.update_one(
            {"sku": product.sku}, update_dict)
        return bool(result.modified_count)

    def delete(self, field: str, key) -> bool:
        result = self.__collection.delete_one({field: key})
        return bool(result.deleted_count)

    def increment_anonymous_views(self, product: Product) -> Product:
        product.anonymous_queries = increment_anonymous_queries(
            product.anonymous_queries)
        self.update(product)
        return self.get_by_id("sku", product.sku)