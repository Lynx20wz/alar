from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Path, Response

from deps import user_service_deps
from exceptions import NotCorrectPassword, UserAlreadyExists, UserNotFound
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


@auth_router.post('/login')
async def login(
    response: Response,
    service: user_service_deps,
    data: UserLoginData = Form(),
) -> BaseResponse[UserInfo]:
    try:
        user = await service.login(data.username, data.password)
    except UserNotFound:
        return BaseResponse(success=False, msg='User not found')
    except NotCorrectPassword:
        return BaseResponse(success=False, msg='Not correct password')

    await set_auth_cookies(response, user)
    return BaseResponse(data=UserInfo.model_validate(user))


@auth_router.post('/user', status_code=201)
async def register(
    response: Response,
    service: user_service_deps,
    data: UserRegisterData = Form(),
) -> BaseResponse[UserInfo]:
    try:
        user = await service.add_user(data)
    except UserAlreadyExists:
        return BaseResponse(success=False, msg='User already exists')

    await set_auth_cookies(response, UserModel(id=user.id, username=user.username))
    return BaseResponse(data=UserInfo.model_validate(user))


@auth_router.get('/exists', response_model=UserExistsResponse)
async def check_user_exists(
    service: user_service_deps,
    user_id: Annotated[Optional[int], Path(..., description='Have priority over username')] = None,
    username: Optional[str] = None,
) -> UserExistsResponse:
    if not user_id and not username:
        raise HTTPException(status_code=422, detail='user_id or username must be provided')

    if await service.check_exists(user_id, username):
        return UserExistsResponse(exists=True)
    return UserExistsResponse(exists=False)
