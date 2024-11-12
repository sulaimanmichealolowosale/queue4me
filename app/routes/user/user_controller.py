from fastapi.routing import APIRouter
from fastapi import Depends, status
from app.models.user import Queuer
from app.routes.user.user_service import UserService
from app.utils.oauth2 import get_current_queuer, get_current_user, get_current_admin


user_service = UserService()

router = APIRouter(
    prefix="/api/user",
    tags=['User']
)

@router.post('/queuer', status_code=status.HTTP_201_CREATED)
async def update_queuer_profile(model:Queuer, current_queuer:str = Depends(get_current_queuer)):
    queuer = await user_service.update_queuer_profile(model=model, id=current_queuer['_id'])
    return queuer

@router.get('/{id}')
async def get_user(id:str, current_user:str = Depends(get_current_admin)):
    user = await user_service.get_user(id)
    return user

