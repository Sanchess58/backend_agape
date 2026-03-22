from datetime import datetime
from typing import Any, List
from sqlalchemy.future import select

from app.api.dao.base import BaseDAO
from app.api.events.exceptions import ALREADY_REGISTERED, EVENT_NOT_STARTED, EVENT_LESS_THAN_DAY, NOT_REGISTERED
from app.api.events.models import Event, EventUser
from app.api.events.schemas import EventResponse
from app.api.users.dao import UserDAO
from app.api.users.models import User
from app.api.utils import get_base64_photo
from app.database import async_session_maker
from app.exceptions import NOT_FOUND

HOUR_IN_SECONDS = 60 * 60
DAY_IN_HOURS = 24 * HOUR_IN_SECONDS


class EventDAO(BaseDAO):
    model = Event

    @classmethod
    async def serialize_event(cls, event: Event) -> EventResponse:
        """Сериализует один объект Event в EventResponse с асинхронным полем."""
        base64_photo = await get_base64_photo(event.bucket_name, event.file_path) if event.bucket_name and event.file_path else None
        return EventResponse(
            id=event.id,
            name=event.name,
            description=event.description,
            date_and_time=event.date_and_time,
            reward=event.reward,
            location=event.location,
            photo_url=base64_photo,
        )

    @classmethod
    async def serialize_event_list(cls, events: List[Event]) -> List[EventResponse]:
        """Сериализует список объектов Event."""
        return [
            EventResponse(
                id=event.id,
                name=event.name,
                description=event.description,
                date_and_time=event.date_and_time,
                reward=event.reward,
                location=event.location,
                photo_url=None,
            ) for event in events
        ]

    @classmethod
    async def list_between_dates(cls, date_from: datetime, date_to: datetime) -> list[Event]:
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.date_and_time.between(date_from, date_to))
            res = await session.execute(query)
            return await cls.serialize_event_list(res.scalars().all())

    @classmethod
    async def get(cls, pk: int) -> EventResponse:
        event = await cls.find_one_or_none_by_id(pk)
        return await cls.serialize_event(event)


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
    async def cancel(cls, user_id: int, **data: dict[str, Any]):
        async with async_session_maker() as session:
            async with session.begin():
                event_users = await cls.find_all(user_id=user_id, **data)
                if not event_users:
                    raise NOT_REGISTERED
                event: Event = await EventDAO.find_one_or_none_by_id(data["event_id"])

                if (event.date_and_time - datetime.now()).total_seconds() <= DAY_IN_HOURS:
                    raise EVENT_LESS_THAN_DAY

                await cls.delete(user_id=user_id, **data)

    @classmethod
    async def confirmation(cls, **data: dict[str, Any]) -> int:
        async with async_session_maker() as session:
            async with session.begin():
                event_user: EventUser | None = await cls.find_one_or_none(
                    **{"user_id": data["user_id"], "event_id": data["event_id"]}
                )
                if not event_user or event_user.attended is not None:
                    raise NOT_FOUND

                event: Event = await EventDAO.find_one_or_none_by_id(data["event_id"])
                if event.date_and_time > datetime.now():
                    raise EVENT_NOT_STARTED

                attented = data["attended"]
                session.add(event_user)
                event_user.attended = attented

                user: User = await UserDAO.find_one_or_none_by_id(data["user_id"])
                session.add(user)

                if not attented:
                    user.balance -= event.reward // 2

                if user and event and attented:
                    user.balance += event.reward
                await session.commit()

                return event_user

    @classmethod
    async def my(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(Event)
                .join(EventUser)
                .where(EventUser.user_id == user_id)
            )
            res = await session.execute(query)
            return await EventDAO.serialize_event_list(res.scalars().all())
