import jwt
import datetime
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from typing import Dict

from app.api.authentication.constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.api.authentication.custom_http_bearer import CustomHTTPBearer
from app.api.authentication.exceptions import CREDENTIAL_EXCEPTION, CREDENTIAL_EXPIRED, CREDENTIAL_PAYLOAD
from app.api.users.models import User

oauth2_scheme = CustomHTTPBearer(scheme_name="JWT Token")


def create_jwt_token(data: Dict):
    """
    Функция для создания JWT токена. Мы копируем входные данные, добавляем время истечения и кодируем токен.
    """
    to_encode = data.copy()
    expire = datetime.datetime.now() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    """
    Функция для извлечения информации о пользователе из токена. Проверяем токен и извлекаем утверждение о пользователе.
    """
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload:
            raise CREDENTIAL_PAYLOAD
        return payload
    except jwt.exceptions.ExpiredSignatureError:
        raise CREDENTIAL_EXPIRED
    except jwt.exceptions.DecodeError:
        raise CREDENTIAL_EXCEPTION


def get_data_for_jwt(user: User) -> dict:
    return {
        "id": user.id,
        "login": user.login,
        "telegram_id": user.telegram_id,
    }
