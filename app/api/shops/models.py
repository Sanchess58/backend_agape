from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.annotations import int_pk, str_null_true


class ShopItem(Base):
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str_null_true]
    photo: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[int]
