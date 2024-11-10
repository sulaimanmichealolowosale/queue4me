from fastapi.routing import APIRouter
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.auth import UserModel
from .auth_service import AuthService

router = APIRouter(
    prefix="/api/auth",
    tags=['Auth']
)

auth_service = AuthService()

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(model:UserModel):
    user = await auth_service.register(model)
    return user

@router.post('/login')
async def login(model:OAuth2PasswordRequestForm=Depends()):
    user =await auth_service.login(model)
    return user