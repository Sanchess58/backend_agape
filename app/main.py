from fastapi import FastAPI
from sqladmin import Admin

from admin_auth import AdminAuth
from api.events.admin import EventAdmin, EventUserAdmin
from api.events.routes import router as event_router
from api.shops.routes import router as shop_router
from api.users.admin import UserAdmin
from api.users.routes import router as user_router
from config import settings
from database import engine

app = FastAPI(title="My FastAPI App")

app.include_router(event_router)
app.include_router(user_router)
app.include_router(shop_router)

admin_auth_backend = AdminAuth(secret_key=settings.ADMIN_SECRET)
admin = Admin(app, engine, authentication_backend=admin_auth_backend)

admin.add_view(UserAdmin)
admin.add_view(EventAdmin)
admin.add_view(EventUserAdmin)
