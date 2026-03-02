from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlalchemy.future import select
from app.api.users.models import User
from app.database import async_session_maker
from app.config import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        login = form["username"]
        password = form["password"]

        async with async_session_maker() as session:
            user = await session.scalar(
                select(User).where(User.login == login)
            )
            if user and user.is_admin and password == settings.ADMIN_PASS:
                request.session.update({"token": str(user.id)})
                return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        if not (token := request.session.get("token")):
            return False

        async with async_session_maker() as session:
            user = await session.get(User, int(token))
            if user and user.is_admin:
                return True
        return False
