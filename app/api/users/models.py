from datetime import date

from sqlalchemy import BigInteger, text, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.annotations import int_pk, str_uniq


class User(Base):
    id: Mapped[int_pk]
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str]
    login: Mapped[str_uniq]
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    balance: Mapped[int] = mapped_column(server_default=text('0'))
    birthday: Mapped[date]
    password: Mapped[str] = mapped_column(String, nullable=True)
