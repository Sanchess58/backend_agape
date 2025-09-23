from pydantic import BaseModel
from typing import Optional
from datetime import date


class UserBase(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str
    login: str
    birthday: date | None


class UserResponse(UserBase):
    is_admin: bool
    id: int

    class Config:
        from_attributes = True


class LoginUser(BaseModel):
    login: str
    password: str


class LoginUserResponse(BaseModel):
    access_token: str


class ChangePassword(BaseModel):
    password: str
    new_password: str


class TelegramIdLogin(BaseModel):
    telegram_id: int
