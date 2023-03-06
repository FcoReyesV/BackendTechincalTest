from fastapi import APIRouter, HTTPException, status, Depends
from passlib.context import CryptContext
from admin.domain.admin_model import Admin
from admin.infrastructure.mongodb_admin_repository import MongoDBSuperAdminRepository
from admin.application.admin_service import AdminService
from login.infrastructure.auth_service import AuthService
from login.infrastructure.mongodb_user_repository import MongoDBUserRepository
import login.infrastructure.login_user_api_fastapi as loginapi
#from admin.infrastructure.fakedb_superadmin_repository import FakeDBSuperAdminRepository


router = APIRouter(prefix="/admin",
                   tags=["admin"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

# Setup admin service with MongoDBAdminRepository
#admin_repo: ISuperAdminRepository = FakeDBSuperAdminRepository()
admin_service = AdminService(MongoDBSuperAdminRepository("MONGO_URI"))
auth_service = AuthService(MongoDBUserRepository("MONGO_URI"))
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def check_if_user_is_superadmin():
    admin_email = await loginapi.auth_user()
    if not admin_email:
        return False
    admin = admin_service.get_admin_by_id("email", admin_email)
    if not admin or not admin.is_superadmin:
        return False
    return True


@router.post("/", response_model=Admin)
async def create_admin(admin: Admin, is_superadmin: bool = Depends(check_if_user_is_superadmin)):
    check_if_can_make_changes(is_superadmin)
    admin.password = crypt.hash(admin.password)
    result = admin_service.create_admin(admin)
    if result:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="Admin created")
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin could not be created")
    
@router.post("/superadmin/", response_model=Admin)
async def create_superadmin(admin: Admin):
    admin.is_superadmin = True
    admin.password = crypt.hash(admin.password)
    result = admin_service.create_admin(admin)
    if result:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="Admin created")
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin could not be created")

@router.get("/{admin_id}")
async def get_admin(admin_id: str, is_superadmin: bool = Depends(check_if_user_is_superadmin)) -> Admin:
    check_if_can_make_changes(is_superadmin)
    admin = admin_service.get_admin_by_id("email", admin_id)
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found")
    return admin


@router.get("/")
async def get_all_admins(is_superadmin: bool = Depends(check_if_user_is_superadmin)) -> list[Admin]:
    check_if_can_make_changes(is_superadmin)
    admins = admin_service.get_all_admins()
    if len(admins) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admins not found")
    return admins
        
    

@router.put("/")
async def update_admin(admin: Admin, is_superadmin: bool = Depends(check_if_user_is_superadmin)):
    check_if_can_make_changes(is_superadmin)
    if admin.password:
        admin.password = crypt.hash(admin.password)
    result = admin_service.update_admin(admin)
    if result:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"Admin with email {admin.email} updated in db")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with email {admin.email} could not be updated")

@router.delete("/{admin_id}")
async def delete_admin(admin_id: str, is_superadmin: bool = Depends(check_if_user_is_superadmin)):
    check_if_can_make_changes(is_superadmin)
    result = admin_service.delete_admin("email", admin_id)
    if result:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"Admin with id {admin_id} deleted from db")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id {admin_id} could not be deleted")

def check_if_can_make_changes(is_superadmin: bool):
    if not is_superadmin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to make changes to admins"
        )
