from datetime import datetime
from typing import Any, List
from sqlalchemy.future import select

from app.api.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import NOT_FOUND
from api.users.models import User
from api.users.dao import UserDAO
from .exceptions import ALREADY_REGISTERED, EVENT_NOT_STARTED
from .models import Event, EventUser
from .schemas import EventResponse
from .utils import get_presigned_url


class EventDAO(BaseDAO):
    model = Event

    @classmethod
    async def serialize_event(cls, event: Event) -> EventResponse:
        """Сериализует один объект Event в EventResponse с асинхронным полем."""
        photo_url = await get_presigned_url(event.bucket_name, event.file_path) if event.bucket_name and event.file_path else None

        return EventResponse(
            id=event.id,
            name=event.name,
            description=event.description,
            date_and_time=event.date_and_time,
            reward=event.reward,
            location=event.location,
            photo_url=photo_url,
        )

    @classmethod
    async def serialize_event_list(cls, events: List[Event]) -> List[EventResponse]:
        """Сериализует список объектов Event."""
        return [await cls.serialize_event(event) for event in events]

    @classmethod
    async def list_between_dates(cls, date_from: datetime, date_to: datetime) -> list[Event]:
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.date_and_time.between(date_from, date_to))
            res = await session.execute(query)
            return await cls.serialize_event_list(res.scalars().all())


class EventUserDAO(BaseDAO):
    model = EventUser

    @classmethod
    async def registration(cls, user_id: int, **data: dict[str, Any]):
        async with async_session_maker() as session:
            async with session.begin():
                event_users = await cls.find_all(user_id=user_id, **data)
                if event_users:
                    raise ALREADY_REGISTERED
                await cls.add(user_id=user_id, **data)

    @classmethod
    async def confirmation(cls, **data: dict[str, Any]) -> None:
        async with async_session_maker() as session:
            async with session.begin():
                event_user: EventUser | None = await cls.find_one_or_none(**{"user_id": data["user_id"], "event_id": data["event_id"]})
                if not event_user or event_user.attended is not None:
                    raise NOT_FOUND

                attented = data["attended"]
                session.add(event_user)
                event_user.attended = attented

                user: User = await UserDAO.find_one_or_none_by_id(data["user_id"])
                event: Event = await EventDAO.find_one_or_none_by_id(data["event_id"])
                session.add(user)

                if event.date_and_time > datetime.now():
                    raise EVENT_NOT_STARTED

                if not attented:
                    user.balance -= event.reward // 2
                    return

                if user and event:
                    user.balance += event.reward

    @classmethod
    async def my(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(Event)
                .join(EventUser)
                # .where(Event.date_and_time >= datetime.now(), EventUser.user_id == user_id)
                .where(EventUser.user_id == user_id)
            )
            res = await session.execute(query)
            return await EventDAO.serialize_event_list(res.scalars().all())
