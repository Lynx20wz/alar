__all__ = ('jwt_generator', 'JWTBearer')

import datetime

from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer
from jose import jwt as jose_jwt, JWTError
from config import config

from database import DataBaseCrud
from deps import get_db_session


class JWTGenerator:
    def _generate_jwt_token(
        self,
        *,
        subject: str,
        jwt_data: dict[str, str] = None,
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

    def decode_jwt(self, token: str) -> dict:
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
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.db = DataBaseCrud()

    async def __call__(self, request: Request, session = Depends(get_db_session)):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=401, detail='Invalid authentication scheme.')
            jwt_data = jwt_generator.decode_jwt(credentials.credentials)
            if not jwt_data:
                raise HTTPException(status_code=401, detail='Invalid token or expired token.')
            db_user = await self.db.get_user_by_id(session, int(jwt_data['sub']))
            if not db_user or db_user.username != request.cookies.get('username'):
                raise HTTPException(status_code=401, detail='User not found.')
        else:
            raise HTTPException(status_code=401, detail='Invalid authorization code.')
