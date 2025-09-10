from fastapi.exceptions import HTTPException
from fastapi import status

CREDENTIAL_PAYLOAD = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="no payload",
    headers={"WWW-Authenticate": "Bearer"},
)

CREDENTIAL_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="decode",
    headers={"WWW-Authenticate": "Bearer"},
)

CREDENTIAL_EXPIRED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="expired",
    headers={"WWW-Authenticate": "Bearer"},
)