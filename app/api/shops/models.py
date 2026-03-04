from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.annotations import int_pk, str_null_true


class ShopItem(Base):
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str_null_true]
    bucket_name: Mapped[str] = mapped_column(nullable=True)
    file_path: Mapped[str] = mapped_column(nullable=True)
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[int]
