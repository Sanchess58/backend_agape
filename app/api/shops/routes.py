from fastapi import APIRouter, Depends, Response, status

from .schemas import ShopItemBase, ShopItemResponse, ShopItemBuy
from .dao import ShopDAO
from api.users.dao import UserDAO
from api.authentication.dependings import get_user_from_token
from api.decorators import admin_required


router = APIRouter(prefix="/shops", tags=["Shops"])


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
