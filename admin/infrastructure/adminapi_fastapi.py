from fastapi import APIRouter, HTTPException, status
from admin.domain.admin_model import Admin
from admin.application.superadmin_repository import ISuperAdminRepository
from admin.infrastructure.mongodb_admin_repository import MongoDBSuperAdminRepository
from admin.application.admin_service import AdminService
from passlib.context import CryptContext
#from admin.infrastructure.fakedb_superadmin_repository import FakeDBSuperAdminRepository


router = APIRouter(prefix="/admin",
                   tags=["admin"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

# Setup admin service with MongoDBAdminRepository
#admin_repo: ISuperAdminRepository = FakeDBSuperAdminRepository()
admin_repo: ISuperAdminRepository = MongoDBSuperAdminRepository("MONGO_URI")
admin_service = AdminService(admin_repo)
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=Admin)
async def create_admin(admin: Admin):
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
async def get_admin(admin_id: str) -> Admin:
    admin = admin_service.get_admin_by_id("email", admin_id)
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, 
            detail="Admin not found")
    return admin


@router.get("/")
async def get_all_admins() -> list[Admin]:
    admins = admin_service.get_all_admins()
    if len(admins) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Admins not found")
    return admins
        
    

@router.put("/")
async def update_admin(admin: Admin):
    if admin.password:
        admin.password = crypt.hash(admin.password)
    result = admin_service.update_admin(admin)
    if result:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"Admin with email {admin.email} updated in db")
    else:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Admin with email {admin.email} could not be updated")

@router.delete("/{admin_id}")
async def delete_admin(admin_id: str):
    result = admin_service.delete_admin("email", admin_id)
    if result:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"Admin with id {admin_id} deleted from db")
    else:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Admin with id {admin_id} could not be deleted")

