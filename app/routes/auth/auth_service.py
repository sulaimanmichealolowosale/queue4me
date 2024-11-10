from datetime import timedelta
from bson import ObjectId
from fastapi import status
from app.config.db import motor_db
from app.models.auth import UserModel
from app.utils.messages import server_error
from app.schemas.schema import user_serializer
from app.utils.oauth2 import credentials_exception
from app.utils.password_crypt import get_password_hash, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.oauth2 import create_access_token

# {
#   "username": "client",
#   "email": "client@client.com",
#   "verification_code": "",
#   "role": "client",
#   "password": "sulaiman",
#   "created_at": "2024-11-07T09:05:43.348977"
# }

class AuthService:
    def __init__(self) -> None:
        self.collection_name = motor_db['user']

    
    async def register(self, model:UserModel):

        existing_user = await self.collection_name.find_one({"email":model.email})
        if existing_user is not None:
            server_error(status.HTTP_409_CONFLICT, f"User with email: {model.email} already exists")
        try:
            hashed_password =  get_password_hash(model.password)
            model.password = hashed_password
            user = await self.collection_name.insert_one(model.model_dump())
            inserted_user = await self.collection_name.find_one({"_id":ObjectId(user.inserted_id)})
            return user_serializer(inserted_user)
        except Exception as e:
            server_error(status.HTTP_500_INTERNAL_SERVER_ERROR, e)
        return
    
    async def login(self, model:OAuth2PasswordRequestForm):

        existing_user = await self.collection_name.find_one({"email":model.username})
        if existing_user is None or not verify_password(model.password, existing_user['password']):
            raise credentials_exception()
        
        try:
            data = {
                "id":str(existing_user['_id']), 
                "username":existing_user['username'],
                "email":existing_user['email'],
                 }
            access_token = create_access_token(data=data)
            refresh_token = create_access_token(data=data, expires_delta=timedelta(days=1))
            return {
                "user":user_serializer(existing_user),
                "access_token":access_token,
                "refresh_token":refresh_token,
            }
        except Exception as e:
            server_error(status.HTTP_500_INTERNAL_SERVER_ERROR, e)
    