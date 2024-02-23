from pydantic import BaseModel
from datetime import datetime


class Item(BaseModel):
    id: str = None
    title: str
    timestamp: datetime
    description: str | None = None
