from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from .schemas import EventResponse, EventUsersResponse, EventBase, EventRegister, EventConfirmation
from .dao import EventDAO, EventUserDAO
from api.authentication.dependings import get_user_from_token
from api.decorators import admin_required

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/", response_model=list[EventResponse])
async def get_events(token: str = Depends(get_user_from_token)):
    return await EventDAO.all_records()


@router.post("/", response_model=EventResponse)
@admin_required
async def create_event(data: EventBase, token: str = Depends(get_user_from_token)):
    return await EventDAO.add(**data.model_dump(exclude_unset=True))


@router.post("/register")
async def event_register(data: EventRegister, token: str = Depends(get_user_from_token)):
    data = data.model_dump(exclude_unset=True)
    await EventUserDAO.registration(user_id=token["id"], **data)
    return JSONResponse(content={"success": "Registration for the event was successful"}, status_code=status.HTTP_200_OK)


@router.post("/confirmation")
async def event_confirmation(data: EventConfirmation, token: str = Depends(get_user_from_token)):
    await EventUserDAO.confirmation(**data.model_dump(exclude_unset=True))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{event_id}/users", response_model=list[EventUsersResponse])
@admin_required
async def event_users(event_id: int, token: str = Depends(get_user_from_token)):
    return await EventUserDAO.find_all(id=event_id)
