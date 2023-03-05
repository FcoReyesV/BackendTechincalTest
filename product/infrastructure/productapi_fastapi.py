from fastapi import APIRouter, HTTPException, status
from product.domain.product_model import Product
from product.application.product_repository import IProductRepository
from product.application.product_service import ProductService
from product.application.anonymous_user_service import AnonymousUserService
from product.infrastructure.mongodb_product_repository import MongoDBProductRepository
#from product.infrastructure.fakedb_product_repository import FakeDBProductRepository


router = APIRouter(prefix="/product",
                   tags=["product"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})
#product_repo: IProductRepository = FakeDBProductRepository()
product_repo: IProductRepository = MongoDBProductRepository("MONGO_URI")
product_service = ProductService(product_repo)
anonymous_service = AnonymousUserService(product_repo)

@router.post("/", response_model=Product)
async def create_product(product: Product):
    result = product_service.create_product(product)
    if result:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="Product created")
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product could not be created")


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str) -> Product:
    product = product_service.get_product_by_id("sku", product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found")
    product_query_updated = anonymous_service.increment_anonymous_views(product)
    return product_query_updated


@router.get("/")
async def get_all_products() -> list[Product]:
    products = product_service.get_all_products()
    if len(products) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Admins not found")
    return products


@router.put("/")
async def update_product(product: Product):
    result = product_service.update_product(product)
    if result:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"Product with sku {product.sku} updated in db")
    else:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Product with email {product.sku} could not be updated")


@router.delete("/{product_id}")
async def delete_product(product_id: str):
    result = product_service.delete_product("sku", product_id)
    if result:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"Product with id {product_id} deleted from db")
    else:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Product with id {product_id} could not be deleted")
