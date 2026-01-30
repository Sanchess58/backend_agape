from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str
    login: str
    birthday: date | None
    church: str | None
    referral_source: str | None
    gender: str


class UserResponse(UserBase):
    balance: int
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
