from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class Status(Enum):
    pending = "pending"
    accepted = "accepted"
    completed = "completed"

class QueueModel(BaseModel):
    duration: float = Field(200, description="duration in minutes")
    address: str = "Access Bank Choba, Port Harcourt"
    zip_code: str = '103101'
    status:Status = Status.pending
    created_at:datetime= datetime.now()
    
    class Config:
        use_enum_values = True



# class ProcessQueue(QueueModel):
#     request_id:str
#     queuer_id:str
#     total:str