from pydantic import BaseModel, Field
from datetime import datetime

class Queuer(BaseModel):
    duration: int = Field(60, description="Duration in minutes")
    rate: float = Field(500, description="Rate per hour")
    zip_code: str = Field('103101', description="ZIP code of the queuing location")
    created_at:datetime= datetime.now()

