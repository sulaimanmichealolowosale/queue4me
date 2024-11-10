from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Queuer(BaseModel):
    duration: str = "1 hour"
    rate: float = 500
    zip_code: str = '103101'
    created_at:datetime= datetime.now()
