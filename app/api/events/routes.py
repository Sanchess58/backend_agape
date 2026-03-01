from datetime import date, datetime, time, timezone

from fastapi import APIRouter, Depends, Form, File, Response, status, UploadFile
from fastapi.responses import JSONResponse

from app.api.s3_storage import S3Client
from app.api.authentication.dependings import get_user_from_token
from app.api.decorators import admin_required
from app.config import settings
from app.api.events.schemas import (
    EventConfirmation,
    EventRegister,
    EventRegisterResponse,
    EventResponse,
    EventUsersResponse,
)
from app.api.events.dao import EventDAO, EventUserDAO

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/{event_id}/", response_model=EventResponse)
async def get_events(event_id: int, token: str = Depends(get_user_from_token)):
    return await EventDAO.find_one_or_none(id=event_id)


@router.get("/", response_model=list[EventResponse])
async def get_events(date_from: date, date_to: date, token: str = Depends(get_user_from_token)):
    start = datetime.combine(date_from, time.min)
    end = datetime.combine(date_to, time.max)
    return await EventDAO.list_between_dates(start, end)


@router.post("/", response_model=EventResponse)
@admin_required
async def create_event(
    name: str = Form(),
    description: str = Form(None),
    date_and_time: datetime = Form(),
    reward: int = Form(None),
    location: str = Form(None),
    photo: UploadFile = File(),
    token: str = Depends(get_user_from_token),
):

    await S3Client(
        access_key=settings.S3_ACCESS_KEY,
        secret_key=settings.S3_SECRET_KEY,
        endpoint_url=settings.S3_URL,
        bucket_name=settings.BUCKET_NAME,
        region_name=settings.S3_REGION,
    ).upload_file(file=photo)

    data = {
        "name": name,
        "description": description,
        "date_and_time": date_and_time.astimezone(timezone.utc).replace(tzinfo=None),
        "reward": reward,
        "location": location,
        "bucket_name": "agape-storage",
        "file_path": photo.filename,
    }
    return await EventDAO.add(**data)


@router.post("/register", response_model=EventRegisterResponse)
async def event_register(data: EventRegister, token: str = Depends(get_user_from_token)):
    data = data.model_dump(exclude_unset=True)
    await EventUserDAO.registration(user_id=token["id"], **data)
    return JSONResponse(content={"success": "Registration for the event was successful"}, status_code=status.HTTP_200_OK)


@router.post("/confirmation", status_code=status.HTTP_204_NO_CONTENT)
async def event_confirmation(data: EventConfirmation, token: str = Depends(get_user_from_token)):
    await EventUserDAO.confirmation(**data.model_dump(exclude_unset=True))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{event_id}/users", response_model=list[EventUsersResponse])
@admin_required
async def event_users(event_id: int, token: str = Depends(get_user_from_token)):
    return await EventUserDAO.find_all(event_id=event_id)


@router.get("/my", response_model=list[EventResponse])
async def my_events(token: str = Depends(get_user_from_token)):
    return await EventUserDAO.my(user_id=token["id"])
