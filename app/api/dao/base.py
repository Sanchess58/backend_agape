from typing import Any

from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            data_id: Критерии фильтрации в виде идентификатора записи.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by: dict[str, Any]):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, where=None, **filter_by: dict[str, Any]):
        """
        Асинхронно находит и возвращает все экземпляры модели, удовлетворяющие указанным критериям.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Список экземпляров модели.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            if where is not None:
                query = query.where(where)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values: dict[str, Any]):
        """
        Асинхронно создает новый экземпляр модели с указанными значениями.

        Аргументы:
            **values: Именованные параметры для создания нового экземпляра модели.

        Возвращает:
            Созданный экземпляр модели.
        """
        async with async_session_maker() as session:
            async with session.begin():
                instance = cls.model(**values)
                session.add(instance)
            await session.refresh(instance)
            return instance
        
    @classmethod
    async def delete(cls, **values: dict[str, Any]):
        """
        Асинхронно удаляет экземпляр модели с указанными значениями.

        Аргументы:
            **values: Именованные параметры для удаления экземпляра модели.

        Возвращает: None.
        """
        async with async_session_maker() as session:
            async with session.begin():
                instance = await cls.find_one_or_none(**values)
                if instance:
                    await session.delete(instance)

    @classmethod
    async def all_records(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()
