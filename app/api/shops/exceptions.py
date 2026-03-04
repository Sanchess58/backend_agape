from fastapi.exceptions import HTTPException
from fastapi import status

INSUFFICIENT_FUNDS = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Недостаточно средств для покупки",
)

WRONG_QUANTITY = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Некорректное количество",
)
