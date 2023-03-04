from fastapi import APIRouter, HTTPException, status
from admin.domain.admin_model import Admin
from admin.application.superadmin_repository import ISuperAdminRepository, AdminRepositoryException
from admin.infrastructure.mongodb_admin_repository import MongoDBSuperAdminRepository
from admin.application.admin_service import AdminService
#from admin.infrastructure.fakedb_superadmin_repository import FakeDBSuperAdminRepository


router = APIRouter(prefix="/admin",
                   tags=["admin"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

# Setup admin service with MongoDBAdminRepository
admin_repo: ISuperAdminRepository = MongoDBSuperAdminRepository("MONGO_URI")
#admin_repo: ISuperAdminRepository = FakeDBSuperAdminRepository()
admin_service = AdminService(admin_repo)


@router.post("/", response_model=Admin)
async def create_admin(admin: Admin):
    try:
        result = admin_service.create_admin(admin)
        if result:
            raise HTTPException(
                status_code=status.HTTP_201_CREATED, 
                detail="User created")
    except AdminRepositoryException as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{ex}"
        ) from ex
    

@router.get("/{admin_id}")
async def get_admin(admin_id: str) -> Admin:
    try:
        admin = admin_service.get_admin_by_id("email", admin_id)
        if admin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    except AdminRepositoryException as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
    return admin

@router.get("/")
async def get_all_admins() -> list[Admin]:
    try:
        admins = admin_service.get_all_admins()
    except AdminRepositoryException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return admins


@router.put("/{admin_id}")
async def update_admin(admin: Admin):
    try:
        result = admin_service.update_admin(admin)
        if result:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f"Admin with email {admin.email} updated from db")
    except AdminRepositoryException as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(ex)) from ex


@router.delete("/{admin_id}")
async def delete_admin(admin_id: str):
    try:
        result = admin_service.delete_admin("email", admin_id)
        if result:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f"Admin with id {admin_id} deleted from db")
    except AdminRepositoryException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
