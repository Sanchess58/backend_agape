from fastapi.exceptions import HTTPException
from fastapi import status

EVENT_NOT_STARTED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Мероприятие еще не началось",
)

ALREADY_REGISTERED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Вы уже зарегистрированы на мероприятие"
)

NOT_REGISTERED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Вы не зарегистрированы на мероприятие"
)

EVENT_LESS_THAN_DAY = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="До начала мероприятия осталось меньше суток",
)
