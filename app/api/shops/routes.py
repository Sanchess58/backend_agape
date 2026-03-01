from fastapi import APIRouter, Depends, Response, status

from app.api.shops.schemas import ShopItemBase, ShopItemResponse, ShopItemBuy
from app.api.shops.dao import ShopDAO
from app.api.users.dao import UserDAO
from app.api.authentication.dependings import get_user_from_token
from app.api.decorators import admin_required


router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ShopItemResponse])
async def get_shop_items(token: str = Depends(get_user_from_token)):
    return await ShopDAO.all_records()


@router.post("", response_model=ShopItemResponse)
@admin_required
async def create_shop_item(data: ShopItemBase, token: str = Depends(get_user_from_token)):
    return await ShopDAO.add(**data.model_dump(exclude_unset=True))


@router.post("/buy", response_model=ShopItemResponse)
async def buy_shop_item(data: ShopItemBuy, token: str = Depends(get_user_from_token)):
    user = await UserDAO.find_one_or_none_by_id(token["id"])

    await ShopDAO.buy(user=user, **data.model_dump(exclude_unset=True))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
