from pydantic import BaseModel
from datetime import datetime
class OrderResponse:
    id: int
    client_name: str
    arrival_time: datetime
    parts_to_change: str
    status: str

    class Config:
        from_attributes = True
