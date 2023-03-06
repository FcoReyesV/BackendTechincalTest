from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from login.infrastructure.auth_service import AuthService
from login.application.user_repository import IUserRepository
from login.infrastructure.mongodb_user_repository import MongoDBUserRepository


router = APIRouter(prefix="/login",
                   tags=["login"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})
user_repo: IUserRepository = MongoDBUserRepository("MONGO_URI")
auth_service = AuthService(user_repo)
access_token = None

@router.post("/login/")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    global access_token
    user = auth_service.authenticate_user(
        form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect username or password")
    access_token_created = auth_service.create_access_token(user)
    access_token = access_token_created.access_token
    return {"access_token": access_token_created.access_token, "token_type": "bearer"}


async def auth_user():
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        email = auth_service.get_email_by_token(access_token)
        if email is None:
            raise exception
    except JWTError as exc:
        raise exception from exc
    return email
