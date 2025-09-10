from app.api.dao.base import BaseDAO
from .models import ShopItem
from api.users.models import User
from app.database import async_session_maker
from app.exceptions import NOT_FOUND
from .exceptions import INSUFFICIENT_FUNDS, WRONG_QUANTITY

class ShopDAO(BaseDAO):
    model = ShopItem

    @classmethod
    async def buy(cls, user: User, **data):
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
