from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import JSONResponse

from app.api.authentication.dependings import create_jwt_token, get_data_for_jwt, get_user_from_token
from app.api.decorators import admin_required
from app.api.users.dao import UserDAO
from app.api.users.models import User
from app.api.users.schemas import UserBase, UserResponse, TelegramIdLogin, LoginUserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
@admin_required
async def get_users(ids: list[int] | None = Query(default=None), token: str = Depends(get_user_from_token)):
    if ids:
        return await UserDAO.find_all(where=User.id.in_(ids))
        
    return await UserDAO.all_records()


@router.get("/{telegram_id}", response_model=UserResponse)
async def get_user_by_telegram_id(telegram_id: int, token: str = Depends(get_user_from_token)):
    return await UserDAO.find_one_or_none(telegram_id=telegram_id)


@router.post("/", response_model=UserResponse)
async def create_user(data: UserBase):
    user_data = data.model_dump(exclude_unset=True)
    user = await UserDAO.registration(**user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account already exists")
    return user


@router.post("/login", response_model=LoginUserResponse)
async def user_login(data: TelegramIdLogin):
    check_data = data.model_dump(exclude_unset=True)
    user = await UserDAO.find_one_or_none(**check_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not registered")
    return JSONResponse(content={"token": create_jwt_token(get_data_for_jwt(user))}, status_code=status.HTTP_200_OK)


# @router.post("/change-password")
# async def change_password(data: ChangePassword, token: str = Depends(get_user_from_token)):
#     login_data = data.model_dump(exclude_unset=True)
#     print(login_data)
#     print(token)
#     return Response(status_code=204)
#     # user = await UserDAO.get_user_by_credits(**login_data)
