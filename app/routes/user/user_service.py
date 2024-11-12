from bson import ObjectId
from app.config.db import motor_db
from fastapi import status
from app.models.user import Queuer
from app.utils.messages import server_error
from app.schemas.schema import queuer_profile_serializer, user_serializer



class UserService:
    def __init__(self) -> None:
        self.queuer_collection = motor_db['queuer']
        self.user_collection = motor_db['user']
        self.applied_request_collection = motor_db['applied_request']

    async def update_queuer_profile(self, model:Queuer, id):
        
        try:
            queuer_model = model.model_dump()
            queuer_model['queuer_id']= id

            existing_queuer = await self.queuer_collection.find_one({"queuer_id":id})
            if existing_queuer is not None:
                await self.queuer_collection.find_one_and_update({"queuer_id":id}, {"$set":queuer_model})

            else:
                await self.queuer_collection.insert_one(queuer_model)

            queuer = await self.user_collection.find_one({"_id":ObjectId(id)})
            queuer_profile =await self.queuer_collection.find_one({"queuer_id":id}) 
            return {
                "queuer": user_serializer(queuer),
                "profile":queuer_profile_serializer(queuer_profile)
            }

        except Exception as e:
            server_error(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e="internal server error")
            return
        
    async def get_users(self):
        
        try:
            cursor = self.user_collection.find()
            user = await cursor.to_list(length=None) 
            return user_serializer(user)
        except Exception as e:
            server_error(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e="internal server error")
            return
        
        
    async def get_user(self, id):
        existing_queuer = await self.user_collection.find_one({"queuer_id":id})
        if existing_queuer is not None:
            server_error(status_code=status.HTTP_404_NOT_FOUND, e=f"The user with id: {id} was not found")
        try:
            user = await self.user_collection.find_one({"_id":ObjectId(id)})
            return user_serializer(user)
        except Exception as e:
            server_error(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e="internal server error")
            return