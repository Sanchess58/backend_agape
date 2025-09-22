from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EventResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    date_and_time: datetime
    reward: Optional[int] = None
    photo_url: Optional[str] = None

    class Config:
        from_attributes = True


class EventRegister(BaseModel):
    event_id: int


class EventConfirmation(BaseModel):
    event_id: int
    user_id: int
    attended: bool


class EventUsersResponse(BaseModel):
    user_id: int
    attended: bool | None
