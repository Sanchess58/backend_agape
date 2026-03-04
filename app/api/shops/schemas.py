from pydantic import BaseModel
from typing import Optional


class ShopItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    photo_url: Optional[str] = None
    quantity: int
    price: int


class ShopItemBuy(BaseModel):
    id: int
    quantity: int


class ShopItemResponse(ShopItemBase):
    id: int

    class Config:
        from_attributes = True
