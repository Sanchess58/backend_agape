from datetime import date
from enum import Enum

from sqlalchemy import BigInteger, text, String, Boolean, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.annotations import int_pk, str_uniq


class GenderEnum(str, Enum):
    MALE = "Мужской"
    FEMALE = "Женский"


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
    gender: Mapped[str] = mapped_column(
        String,
        CheckConstraint("gender IN ('Мужской', 'Женский')", name="check_gender"),
        nullable=True,
    )
    church: Mapped[str] = mapped_column(String, nullable=True)
    referral_source: Mapped[str] = mapped_column(String, nullable=True)
