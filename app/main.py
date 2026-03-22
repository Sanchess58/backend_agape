from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from sqladmin import Admin

from app.admin_auth import AdminAuth
from app.api.events.admin import EventAdmin, EventUserAdmin
from app.api.events.routes import router as event_router
from app.api.shops.routes import router as shop_router
from app.api.shops.admin import ShopItemAdmin
from app.api.users.admin import UserAdmin
from app.api.users.routes import router as user_router
from app.config import settings
from app.database import engine

app = FastAPI(title="My FastAPI App")
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.include_router(event_router)
app.include_router(user_router)
app.include_router(shop_router)

admin_auth_backend = AdminAuth(secret_key=settings.ADMIN_SECRET)
admin = Admin(app, engine, authentication_backend=admin_auth_backend)

admin.add_view(UserAdmin)
admin.add_view(EventAdmin)
admin.add_view(EventUserAdmin)
admin.add_view(ShopItemAdmin)
