from fastapi import APIRouter, Depends, Response, status

from .schemas import EventResponse, EventBase, EventRegister, EventConfirmation
from .dao import EventDAO, EventUserDAO
from api.authentication.dependings import get_user_from_token

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/", response_model=list[EventResponse])
async def get_events(token: str = Depends(get_user_from_token)):
    return await EventDAO.all_records()


@router.post("/", response_model=EventResponse)
async def create_event(data: EventBase, token: str = Depends(get_user_from_token)):
    return await EventDAO.add(**data.model_dump(exclude_unset=True))


@router.post("/register")
async def event_register(data: EventRegister, token: str = Depends(get_user_from_token)):
    data = data.model_dump(exclude_unset=True)
    data["user_id"] = token["id"]
    await EventUserDAO.add(**data)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/confirmation")
async def event_confirmation(data: EventConfirmation, token: str = Depends(get_user_from_token)):
    await EventUserDAO.confirmation(**data.model_dump(exclude_unset=True))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
