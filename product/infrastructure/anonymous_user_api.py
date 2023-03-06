from fastapi import APIRouter, HTTPException, status
from product.domain.product_model import Product
from product.application.product_repository import IProductRepository
from product.application.product_service import ProductService
from product.application.anonymous_user_service import AnonymousUserService
from product.infrastructure.mongodb_product_repository import MongoDBProductRepository

product_repo: IProductRepository = MongoDBProductRepository("MONGO_URI")
anonymous_service = AnonymousUserService(product_repo)
product_service = ProductService(product_repo)

router = APIRouter(prefix="/anonymous",
                   tags=["anonymous"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str) -> Product:
    product = product_service.get_product_by_id("sku", product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found")
    product_query_updated = anonymous_service.increment_anonymous_views(
        product)
    return product_query_updated
