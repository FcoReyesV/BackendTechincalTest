from fastapi import APIRouter, HTTPException, status, Depends
from product.domain.product_model import Product
from product.application.product_service import ProductService
from product.infrastructure.mongodb_product_repository import MongoDBProductRepository
from admin.application.admin_service import AdminService
from login.infrastructure.auth_service import AuthService
from login.infrastructure.mongodb_user_repository import MongoDBUserRepository
from admin.infrastructure.mongodb_admin_repository import MongoDBSuperAdminRepository
import login.infrastructure.login_user_api_fastapi as loginapi
from utils.email_service import EmailService
#from product.infrastructure.fakedb_product_repository import FakeDBProductRepository


router = APIRouter(prefix="/product",
                   tags=["product"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})
#product_repo: IProductRepository = FakeDBProductRepository()
MONGO_URI = "MONGO_URI"
product_service = ProductService(MongoDBProductRepository(MONGO_URI))
auth_service = AuthService(MongoDBUserRepository(MONGO_URI))
admin_service = AdminService(MongoDBSuperAdminRepository(MONGO_URI))

async def check_if_admin_can_make_changes():
    admin_email = await loginapi.auth_user()
    if not admin_email:
        return False
    admin = admin_service.get_admin_by_id("email", admin_email)
    if not admin:
        return False
    return True


@router.post("/", response_model=Product)
async def create_product(product: Product, 
                         is_logged_in: bool = Depends(check_if_admin_can_make_changes)):
    check_if_can_make_changes(is_logged_in)
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
async def get_product(product_id: str, 
                      is_logged_in: bool = Depends(check_if_admin_can_make_changes)) -> Product:
    check_if_can_make_changes(is_logged_in)
    check_if_admin_can_make_changes()
    product = product_service.get_product_by_id("sku", product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found")
    return product


@router.get("/")
async def get_all_products(is_logged_in: bool = Depends(check_if_admin_can_make_changes)) -> list[Product]:
    check_if_can_make_changes(is_logged_in)
    products = product_service.get_all_products()
    if len(products) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Admins not found")
    return products


@router.put("/")
async def update_product(product: Product, 
                         is_logged_in: bool = Depends(check_if_admin_can_make_changes)):
    check_if_can_make_changes(is_logged_in)
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
async def delete_product(product_id: str, 
                         is_logged_in: bool = Depends(check_if_admin_can_make_changes)):
    check_if_can_make_changes(is_logged_in)
    result = product_service.delete_product("sku", product_id)
    if result:
        send_email_to_all_admins(product_id)
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"Product with id {product_id} deleted from db")
    else:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Product with id {product_id} could not be deleted")


def check_if_can_make_changes(is_logged_in: bool):
    if not is_logged_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin is not logged in"
        )

def send_email_to_all_admins(sku: str):
    admin_list = admin_service.get_all_admins()
    email_service = EmailService()
    subject = "Product deleted from db"
    message = f"Product with sku {sku} was deleted from products"
    for admin in admin_list:
        email_service.send_an_email(admin.email, subject, message)