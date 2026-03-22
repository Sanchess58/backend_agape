from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EventResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    date_and_time: datetime
    reward: Optional[int] = None
    location: Optional[str] = None
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


class EventRegisterResponse(BaseModel):
    success: str


class EventConfirmationResponse(BaseModel):
    reward: int
    event_name: str
    balance: int
