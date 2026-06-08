__all__ = ('jwt_generator', 'JWTBearer')

import datetime
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request
from jose import JWTError
from jose import jwt as jose_jwt

from config import config
from deps import ServiceFactory
from models import UserModel
from services import UserService


class JWTGenerator:
    def _generate_jwt_token(
        self,
        *,
        subject: str,
        jwt_data: dict[str, str] | None = None,
        expires_delta: datetime.timedelta | None = None,
    ) -> str:
        if expires_delta:
            expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
        else:
            expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
                minutes=config.JWT_MIN
            )

        to_encode = {'sub': subject, 'exp': expire} | (jwt_data or {})
        return jose_jwt.encode(to_encode, key=config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)

    def generate_access_token(self, userid: int) -> str:
        return self._generate_jwt_token(
            subject=str(userid),
            expires_delta=datetime.timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRATION_TIME),
        )

    def decode_jwt(self, token: str) -> dict[str, Any] | None:
        try:
            decoded_token = jose_jwt.decode(
                token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
            )
            return decoded_token
        except JWTError:
            return None


jwt_generator = JWTGenerator()


class JWTBearer:
    def __init__(self, auto_error: bool = True):
        self.auto_error = auto_error

    async def __call__(
        self,
        request: Request,
        service: Annotated[UserService, Depends(ServiceFactory(UserService))],
    ) -> UserModel | None:
        token = await self._get_token(request)

        if not token:
            if self.auto_error:
                raise HTTPException(status_code=401, detail='Not authenticated.')
            return None

        jwt_data = jwt_generator.decode_jwt(token)

        if jwt_data is None:
            if self.auto_error:
                raise HTTPException(status_code=401, detail='Invalid token or expired token.')
            return None

        try:
            user_id = int(jwt_data['sub'])
        except (KeyError, ValueError):
            if self.auto_error:
                raise HTTPException(status_code=401, detail='Invalid token format.')
            return None

        user = await service.get_user_by_id(user_id)

        if not user:
            if self.auto_error:
                raise HTTPException(status_code=401, detail='User not found.')
            return None

        return user

    async def _get_token(self, request: Request) -> str | None:
        if header_auth := request.headers.get('Authorization'):
            try:
                return header_auth.split(' ')[1]
            except IndexError:
                return None
        elif cookie_auth := request.cookies.get('token'):
            return cookie_auth
        return None
