from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Roles(Enum):
    admin = "admin"
    queuer = "queuer"
    client = "client"


class UserModel(BaseModel):
    username:str = Field(min_length=4, max_length=25)
    email:str
    verification_code: Optional[str] = ""
    status:str = "active"
    role: Roles = Roles.admin
    password:str
    created_at:datetime= datetime.now()

    class Config:
        use_enum_values = True