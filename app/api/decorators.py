from fastapi import HTTPException, status
from functools import wraps
from typing import Callable, Any

from app.api.users.dao import UserDAO
from app.api.users.models import User


def admin_required(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        user_pk = kwargs["token"]["id"] if "token" in kwargs else kwargs["id"]
        user: User = await UserDAO.find_one_or_none_by_id(user_pk)

        if not user or not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return await func(*args, **kwargs)
    
    return wrapper
