from schemas import UserExistsResponse
from fastapi import APIRouter, Form, Response

from database import DataBaseCrud
from database.models import UserModel
from deps import session_deps
from jwt import jwt_generator
from schemas import *

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)
db = DataBaseCrud()


async def set_auth_cookies(response, user: UserModel):
    response.set_cookie(
        key='token',
        value=jwt_generator.generate_access_token(user.id),
        httponly=True,
        samesite='none',
        secure=True,
    )

    response.set_cookie(
        key='username',
        value=user.username,
        httponly=True,
        samesite='none',
        secure=True,
    )


@auth_router.post('/login')
async def login(
    response: Response, session: session_deps, data: UserLoginData = Form()
) -> BaseResponse:
    userModel = UserModel(username=data.username, password=data.password)
    user = await db.get_user(session, userModel)
    if not user:
        return BaseResponse(success=False, msg='User not found.')

    if not user.check_password(data.password):
        return BaseResponse(success=False, msg='Not correct password.')
    await set_auth_cookies(response, user)
    return BaseResponse()


@auth_router.get('/exists', response_model=UserExistsResponse)
async def check_user_exists(username: str, session: session_deps) -> UserExistsResponse:
    userModel = UserModel(username=username)
    if not await db.get_user(session, userModel):
        return UserExistsResponse(exists=False, username=username)
    return UserExistsResponse(exists=True, username=username)


@auth_router.post('/user', status_code=201)
async def register(
    response: Response, session: session_deps, data: UserRegisterData = Form()
) -> BaseResponse:
    user = UserModel(
        email=data.email,
        password=data.password,
        username=data.username,
        avatar=await data.avatar.read() if data.avatar else None,
        banner=await data.banner.read() if data.banner else None,
    )
    user_id = await db.add_user(session, user)
    await set_auth_cookies(response, UserModel(id=user_id, username=data.username))
    return BaseResponse()
