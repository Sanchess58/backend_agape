from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime, timezone


class EventBase(BaseModel):
    name: str
    description: Optional[str]
    date_and_time: datetime
    reward: Optional[int] = None

    @field_validator("date_and_time")
    def convert_to_utc(cls, value: datetime) -> datetime:
        return value.astimezone(timezone.utc).replace(tzinfo=None)


class EventResponse(EventBase):
    id: int

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
