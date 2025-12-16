__all__ = ('jwt_generator', 'JWTBearer')

import datetime
from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from jose import JWTError
from jose import jwt as jose_jwt

from config import config
from deps import ServiceFactory
from services import UserService


class JWTGenerator:
    def _generate_jwt_token(
        self,
        *,
        subject: str,
        jwt_data: Optional[dict[str, str]] = None,
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

    def decode_jwt(self, token: str) -> dict | None:
        try:
            decoded_token = jose_jwt.decode(
                token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
            )
            return (
                decoded_token
                if decoded_token['exp'] >= datetime.datetime.now(datetime.timezone.utc).timestamp()
                else None
            )
        except JWTError:
            return {}


jwt_generator = JWTGenerator()


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def _get_token(self, request: Request) -> str | None:
        if header_auth := request.headers.get('Authorization'):
            return header_auth.split(' ')[1]
        elif cookie_auth := request.cookies.get('token'):
            return cookie_auth
        return None

    async def __call__(self, request: Request, service=Depends(ServiceFactory(UserService))):
        await super(JWTBearer, self).__call__(request)

        token = await self._get_token(request)

        if not token:
            raise HTTPException(status_code=401, detail='Not authenticated.')

        jwt_data = jwt_generator.decode_jwt(token)

        if not jwt_data:
            raise HTTPException(status_code=401, detail='Invalid token or expired token.')

        user = await service.get_user_by_id(int(jwt_data['sub']))

        if not user:
            raise HTTPException(status_code=401, detail='User not found.')

        if user.username != request.cookies.get('username'):
            raise HTTPException(status_code=401, detail='Invalid credentials.')

        request.state.user = user
