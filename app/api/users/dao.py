from sqlalchemy.future import select
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
    
    # @classmethod
    # async def change_password(cls, **data):
    #     async with async_session_maker() as session:
    #         login, password, new_password = data.values()

    #         query = select(cls.model).filter_by(login=login, password=hash_password(password))
    #         result = await session.execute(query)
    #         return result.scalar_one_or_none()
