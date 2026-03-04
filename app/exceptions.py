from fastapi.exceptions import HTTPException
from fastapi import status

NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Объект не найден",
)
