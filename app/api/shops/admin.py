from sqladmin import ModelView

from api.shops.models import ShopItem


class ShopItemAdmin(ModelView, model=ShopItem):
    column_list = [ShopItem.id, ShopItem.name, ShopItem.price, ShopItem.quantity]
