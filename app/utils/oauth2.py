from datetime import datetime, timedelta, timezone
from typing import Annotated
from bson import ObjectId
from fastapi import status, HTTPException, Depends

from fastapi.security import OAuth2PasswordBearer
import jwt
from app.models.token import TokenModel
from app.models.auth import Roles
from app.utils.get_env import settings
from app.config.db import motor_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def credentials_exception():
    return  HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception()
        token_data = TokenModel(id=id)
        return token_data
    except jwt.InvalidTokenError:
        raise credentials_exception()
    
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    auth_token = verify_access_token(token)
    current_user = await motor_db['user'].find_one({"_id":ObjectId(auth_token.id)})
    if current_user is None:
        raise credentials_exception()
    return current_user

async def get_current_queuer(token: Annotated[str, Depends(oauth2_scheme)]):
    auth_token = verify_access_token(token)
    queuer = await motor_db['user'].find_one({"_id":ObjectId(auth_token.id), "role":Roles.queuer.value})
    if queuer is None:
        raise credentials_exception()
    return queuer

async def get_current_admin(token: Annotated[str, Depends(oauth2_scheme)]):
    auth_token = verify_access_token(token)
    admin = await motor_db['user'].find_one({"_id":ObjectId(auth_token.id), "role":Roles.admin.value})
    if admin is None:
        raise credentials_exception()
    return admin

async def get_current_client(token: Annotated[str, Depends(oauth2_scheme)]):
    auth_token = verify_access_token(token)
    client = await motor_db['user'].find_one({"_id":ObjectId(auth_token.id), "role":Roles.client.value})
    if client is None:
        raise credentials_exception()
    return client

