from fastapi.routing import APIRouter
from fastapi import Depends, status
from app.models.queue import QueueModel
from app.routes.queue.queue_service import QueueService
from app.utils.oauth2 import get_current_client, get_current_queuer


router = APIRouter(
    prefix='/api/queue',
    tags=['Queue']
)

queue_service = QueueService()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_request(model:QueueModel, current_user:str = Depends(get_current_client)):
    queue = await queue_service.create_request(id=current_user["_id"], model=model)
    return queue

@router.post('/{id}', status_code=status.HTTP_201_CREATED)
async def apply_to_queue(id:str, current_user:str = Depends(get_current_queuer)):
    queue = await queue_service.apply_to_queue(id=id, queuer_id=current_user["_id"])
    return queue

@router.get('/')
async def get_request_by_code(code:str, current_user:str = Depends(get_current_queuer)):
    requests = await queue_service.get_request_by_code(code)
    return requests

@router.get('/client')
async def get_request_by_client(current_user:str = Depends(get_current_client)):
    requests = await queue_service.get_request_by_client(current_user["_id"])
    return requests

@router.get('/applied/client')
async def get_request_by_client(current_user:str = Depends(get_current_client)):
    requests = await queue_service.get_applied_requests_by_client(current_user["_id"])
    return requests