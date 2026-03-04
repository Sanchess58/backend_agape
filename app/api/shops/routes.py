from fastapi import APIRouter, Depends, Form, File, Response, status, UploadFile

from app.api.s3_storage import S3Client
from app.api.shops.schemas import ShopItemResponse, ShopItemBuy
from app.api.shops.dao import ShopDAO
from app.api.users.dao import UserDAO
from app.api.authentication.dependings import get_user_from_token
from app.api.decorators import admin_required
from app.config import settings

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ShopItemResponse])
async def get_shop_items(token: str = Depends(get_user_from_token)):
    return await ShopDAO.get_active_items()


@router.post("", response_model=ShopItemResponse)
@admin_required
async def create_shop_item(
    name: str = Form(),
    description: str = Form(None),
    photo: UploadFile = File(),
    quantity: int = Form(),
    price: int = Form(),
    token: str = Depends(get_user_from_token),
):

    await S3Client(
        access_key=settings.S3_ACCESS_KEY,
        secret_key=settings.S3_SECRET_KEY,
        endpoint_url=settings.S3_URL,
        bucket_name=settings.BUCKET_NAME,
        region_name=settings.S3_REGION,
    ).upload_file(file=photo)

    data = {
        "name": name,
        "description": description,
        "quantity": quantity,
        "price": price,
        "bucket_name": "agape-storage",
        "file_path": photo.filename,
    }
    return await ShopDAO.add(**data)


@router.post("/buy", response_model=ShopItemResponse)
async def buy_shop_item(data: ShopItemBuy, token: str = Depends(get_user_from_token)):
    user = await UserDAO.find_one_or_none_by_id(token["id"])

    await ShopDAO.buy(user=user, **data.model_dump(exclude_unset=True))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
