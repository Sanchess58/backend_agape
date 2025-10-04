from datetime import datetime

from sqlalchemy import ForeignKey, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.annotations import int_pk, str_null_true


class Event(Base):
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    bucket_name: Mapped[str] = mapped_column(nullable=True)
    file_path: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str_null_true]
    date_and_time: Mapped[datetime] = mapped_column(nullable=False)
    location: Mapped[str_null_true]
    reward: Mapped[int] = mapped_column(nullable=False)


class EventUser(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    event_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    attended: Mapped[bool] = mapped_column(Boolean, nullable=True)
