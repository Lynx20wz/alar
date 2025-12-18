from typing import Annotated

from fastapi import APIRouter, Form, Query, Response

from deps import user_service_deps
from jwt import jwt_generator
from models import UserModel
from schemas import *

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


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


@auth_router.post(
    '/login',
    responses={
        401: {'description': 'Incorrect password'},
        404: {'description': 'User not found'},
    },
)
async def login(
    response: Response,
    service: user_service_deps,
    data: UserLoginData = Form(),
) -> BaseResponse[UserInfo]:
    user = await service.login(data.username, data.password)

    await set_auth_cookies(response, user)
    return BaseResponse(data=UserInfo.model_validate(user))


@auth_router.post('/user', status_code=201, responses={409: {'description': 'User already exists'}})
async def register(
    response: Response,
    service: user_service_deps,
    data: UserRegisterData = Form(),
) -> BaseResponse[UserInfo]:
    user = await service.add_user(data)

    await set_auth_cookies(response, UserModel(id=user.id, username=user.username))
    return BaseResponse(data=UserInfo.model_validate(user))


@auth_router.get('/exists', response_model=UserExistsResponse)
async def check_user_exists(
    service: user_service_deps,
    username: Annotated[str, Query(description='The username to check', alias='u')],
) -> UserExistsResponse:
    exists = True if await service.check_exists(username) else False
    return UserExistsResponse(exists=exists)
