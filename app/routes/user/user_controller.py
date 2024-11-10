from fastapi.routing import APIRouter
from fastapi import Depends, status
from app.models.user import Queuer
from app.routes.user.user_service import UserService
from app.utils.oauth2 import get_current_queuer


user_service = UserService()

router = APIRouter(
    prefix="/api/user",
    tags=['User']
)

@router.post('/queuer/{id}', status_code=status.HTTP_201_CREATED)
async def update_queuer_profile(id:str, model:Queuer, current_queuer:str = Depends(get_current_queuer)):
    queuer = await user_service.update_queuer_profile(model=model, id=id)
    return queuer