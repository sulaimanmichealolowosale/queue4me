from datetime import datetime
from bson import ObjectId
from fastapi import status
from app.config.db import motor_db
from app.schemas.schema import queue_request_serializer, list_serializer, applied_request_serializer, user_serializer
from app.models.queue import QueueModel
from app.utils.messages import server_error


class QueueService:
    def __init__(self) -> None:
        self.queue_request_collection = motor_db['queue_request']
        self.applied_request_collection = motor_db['applied_request']
        self.queuer_collection = motor_db['queuer']
        self.user_collection = motor_db['user']
        
        
    async def create_request(self, id, model:QueueModel):
        try:
            queue_model = model.model_dump()
            queue_model['client_id'] = id
            queue = await self.queue_request_collection.insert_one(queue_model)
            inserted_request = await self.queue_request_collection.find_one({"_id":ObjectId(queue.inserted_id)})
            return queue_request_serializer(inserted_request)
        except Exception as e:
            server_error(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e="internal server error")
            return
        
    async def apply_to_queue(self, id:str, queuer_id):
        request = await self.queue_request_collection.find_one({"_id":ObjectId(id)})
        if request is None:
            raise server_error(status_code=status.HTTP_404_NOT_FOUND, e="Queue request not found")
        
        queuer = await self.queuer_collection.find_one({"queuer_id":ObjectId(queuer_id)})
        if queuer is None:
            raise server_error(status_code=status.HTTP_404_NOT_FOUND, e="You need to update your profile first")
        client = await self.user_collection.find_one({"_id":ObjectId(request["client_id"])})
        
        existing_applied_request = await self.applied_request_collection.find_one(
            {
                "request_id": ObjectId(request["_id"]),
                "queuer_id": ObjectId(queuer["queuer_id"]),
            })
        if existing_applied_request is not None:
            updated_applied_request=await self.applied_request_collection.find_one_and_update({
                "request_id": ObjectId(request["_id"]),
                "queuer_id": ObjectId(queuer["queuer_id"]),
            },
            {"$set":{
                "total": int((request["duration"]/60)*queuer["rate"]),
                }
            }                                                          
            )
            print(updated_applied_request)
            return {
                "message":"Application has been updated",
                "request":applied_request_serializer(updated_applied_request),
                "client":user_serializer(client)
                }
        try:
            model = {
           "request_id": request["_id"],
           "client_id": request["client_id"],
           "queuer_id": queuer["queuer_id"],
           "duration": request["duration"],
           "address": request["address"],
           "total": int((request["duration"]/60)*queuer["rate"]),
           "zip_code": request["zip_code"],
           "status":"applied",
           "created_at":datetime.now(),
            }
            applied_request = await self.applied_request_collection.insert_one(model)
            inserted_applied_request = applied_request.inserted_id
            inserted_applied_request = await self.applied_request_collection.find_one({"_id":ObjectId(inserted_applied_request)})
            
            
            return {
                "request":applied_request_serializer(inserted_applied_request),
                "client":user_serializer(client)
                }
        except Exception as e:
            server_error(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e="internal server error")
            return
        
    async def get_request_by_code(self, code:str):
        try:            
            cursor = self.queue_request_collection.aggregate([
                {"$match": { "zip_code": code}}
            ])
            requests = await cursor.to_list(length=None)
            
            if len(requests) == 0:
                cursor = self.queue_request_collection.find()
                requests = await cursor.to_list(length=None)
                return {
                    "message":"No requests found from your location",
                    "requests":list_serializer(requests, queue_request_serializer)
                    }
                
            return {
                    "message":"Requests found from your location",
                    "requests":list_serializer(requests, queue_request_serializer)
                    }

        except Exception as e:
            server_error(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e="internal server error")
        
    async def get_request_by_client(self, id:str):
        try:            
            cursor = self.queue_request_collection.find({ "client_id": id})
            requests = await cursor.to_list(length=None)
            
            return list_serializer(requests, queue_request_serializer)
                   
        except Exception as e:
            server_error(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e="internal server error")
        
    async def get_applied_requests_by_client(self, id):
        try:
            cursor = self.applied_request_collection.find({"client_id":ObjectId(id)})
            requests = await cursor.to_list(length=None)
            return list_serializer(requests, applied_request_serializer)
        except Exception as e:
            server_error(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e="internal server error")
    
    
        
        