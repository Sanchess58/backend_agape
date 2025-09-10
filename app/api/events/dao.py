from datetime import datetime

from app.api.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import NOT_FOUND
from api.users.models import User
from api.users.dao import UserDAO
from .exceptions import ALREADY_REGISTERED, EVENT_NOT_STARTED
from .models import Event, EventUser

class EventDAO(BaseDAO):
    model = Event


class EventUserDAO(BaseDAO):
    model = EventUser

    @classmethod
    async def registration(cls, user_id: int, **data):
        async with async_session_maker() as session:
            async with session.begin():
                event_users = cls.find_all(user_id=user_id, **data)
                if event_users:
                    raise ALREADY_REGISTERED
                cls.add(user_id=user_id, **data)

    @classmethod
    async def confirmation(cls, **data):
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
