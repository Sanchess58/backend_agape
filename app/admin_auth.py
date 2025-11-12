from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlalchemy.future import select
from api.users.models import User
from database import async_session_maker


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        login = form["username"]

        async with async_session_maker() as session:
            user = await session.scalar(
                select(User).where(User.login == login)
            )
            if user and user.is_admin:
                request.session.update({"token": str(user.id)})
                return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        async with async_session_maker() as session:
            user = await session.get(User, int(token))
            if user and user.is_admin:
                return True
        return False
