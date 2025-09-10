from fastapi.exceptions import HTTPException
from fastapi import status

EVENT_NOT_STARTED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="event_not_started",
)
