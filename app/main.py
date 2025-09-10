from fastapi import FastAPI

from api.events.routes import router as event_router
from api.users.routes import router as user_router
from api.shops.routes import router as shop_router


app = FastAPI(title="My FastAPI App")

app.include_router(event_router)
app.include_router(user_router)
app.include_router(shop_router)
