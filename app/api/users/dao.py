from sqlalchemy.future import select
from sqlalchemy import or_
from .models import User
from app.api.dao.base import BaseDAO
from app.database import async_session_maker

from .utils import hash_password


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_user_by_credits(cls, **data):
        async with async_session_maker() as session:
            login, password = data.values()

            query = select(cls.model).filter_by(login=login, password=hash_password(password))
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def registration(cls, **data):
        telegram_id = data["telegram_id"]
        login = data["login"]
 
        if await cls.find_all(where=or_(cls.model.telegram_id == telegram_id, cls.model.login == login)):
            return None
        async with async_session_maker() as session:
            async with session.begin():
                instance = cls.model(**data)
                session.add(instance)
            await session.refresh(instance)
            return instance
    