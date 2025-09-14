from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, Response
from .schemas import UserBase, UserResponse, TelegramIdLogin, LoginUserResponse
from .dao import UserDAO
from .utils import generate_password
from api.authentication.dependings import create_jwt_token, get_data_for_jwt, get_user_from_token
from api.decorators import admin_required

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
@admin_required
async def get_users(token: str = Depends(get_user_from_token)):
    return await UserDAO.all_records()


@router.post("/", response_model=UserResponse)
async def create_user(data: UserBase):
    user_data = data.model_dump(exclude_unset=True)
    return await UserDAO.add(**user_data)


@router.post("/login", response_model=LoginUserResponse)
async def user_login(data: TelegramIdLogin):
    check_data = data.model_dump(exclude_unset=True)
    user = await UserDAO.find_one_or_none(**check_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not registered")
    return JSONResponse(content={"token": create_jwt_token(get_data_for_jwt(user))}, status_code=status.HTTP_200_OK)


# @router.post("/login", response_model=LoginUserResponse)
# async def login(data: LoginUser):
#     login_data = data.model_dump(exclude_unset=True)
#     user = await UserDAO.get_user_by_credits(**login_data)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password or login")
#     return JSONResponse(content={"token": create_jwt_token(get_data_for_jwt(user))}, status_code=status.HTTP_200_OK)


# @router.post("/change-password")
# async def change_password(data: ChangePassword, token: str = Depends(get_user_from_token)):
#     login_data = data.model_dump(exclude_unset=True)
#     print(login_data)
#     print(token)
#     return Response(status_code=204)
#     # user = await UserDAO.get_user_by_credits(**login_data)

    