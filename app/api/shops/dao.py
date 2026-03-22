from typing import List

from sqlalchemy.future import select

from app.api.dao.base import BaseDAO
from app.api.shops.exceptions import INSUFFICIENT_FUNDS, WRONG_QUANTITY
from app.api.shops.models import ShopItem
from app.api.shops.schemas import ShopItemResponse
from app.api.users.models import User
from app.api.utils import get_base64_photo
from app.database import async_session_maker
from app.exceptions import NOT_FOUND


class ShopDAO(BaseDAO):
    model = ShopItem

    @classmethod
    async def serialize_shop_item(cls, shop_item: ShopItem) -> ShopItemResponse:
        """Сериализует один объект ShopItem в ShopItemResponse с асинхронным полем."""
        base64_photo = (
            await get_base64_photo(
                shop_item.bucket_name, shop_item.file_path
            )
            if shop_item.bucket_name and shop_item.file_path
            else None
        )

        return ShopItemResponse(
            id=shop_item.id,
            name=shop_item.name,
            description=shop_item.description,
            quantity=shop_item.quantity,
            price=shop_item.price,
            photo_url=base64_photo,
        )

    @classmethod
    async def serialize_shop_item_list(cls, shop_items: List[ShopItem]) -> List[ShopItem]:
        """Сериализует список объектов ShopItem."""
        return [await cls.serialize_shop_item(shop_item) for shop_item in shop_items]

    @classmethod
    async def buy(cls, user: User, **data) -> None:
        """Метод для покупки товара и списания средств со счета покупателя"""
        async with async_session_maker() as session:
            async with session.begin():
                quantity = data["quantity"]
                shop_item: ShopItem | None = await cls.find_one_or_none_by_id(data["id"])
                if shop_item is None:
                    raise NOT_FOUND

                if quantity > shop_item.quantity or quantity <= 0:
                    raise WRONG_QUANTITY

                total_price = shop_item.price * quantity
                if user.balance < total_price:
                    raise INSUFFICIENT_FUNDS

                user.balance -= total_price
                shop_item.quantity -= quantity
                session.add(user)
                session.add(shop_item)

    @classmethod
    async def get_active_items(cls) -> list[ShopItem]:
        """Получить товары, доступные для покупки"""
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.quantity > 1)
            res = await session.execute(query)
            return await cls.serialize_shop_item_list(res.scalars().all())
