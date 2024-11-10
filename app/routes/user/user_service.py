from bson import ObjectId
from app.config.db import motor_db
from fastapi import status
from app.models.user import Queuer
from app.utils.messages import server_error
from app.schemas.schema import queuer_profile_serializer, user_serializer



class UserService:
    def __init__(self) -> None:
        self.collection_name = motor_db['queuer']
        self._collection_name = motor_db['user']

    async def update_queuer_profile(self, model:Queuer, id):
        
        try:
            queuer_model = model.model_dump()
            queuer_model['queuer_id']= id

            existing_queuer = await self.collection_name.find_one({"queuer_id":id})
            if existing_queuer is not None:
                await self.collection_name.find_one_and_update({"queuer_id":id}, {"$set":queuer_model})
            else:
                await self.collection_name.insert_one(queuer_model)

            queuer = await self._collection_name.find_one({"_id":ObjectId(id)})
            queuer_profile = await self.collection_name.find_one({"queuer_id":id}) 
            return {
                "queuer": user_serializer(queuer),
                "profile":queuer_profile_serializer(queuer_profile)
            }

        except Exception as e:
            server_error(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e="internal server error")