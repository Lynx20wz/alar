from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, Response

from deps import ServiceFactory
from jwt import jwt_generator
from models import UserModel
from schemas import *
from services import UserService

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
    service: Annotated[UserService, Depends(ServiceFactory(UserService))],
    response: Response,
    data: UserLoginData = Form(),
) -> BaseResponse:
    user = await service.repository.get_by(username=data.username, password=data.password)
    if not user:
        return BaseResponse(success=False, msg='User not found.')

    if not user.check_password(data.password):
        return BaseResponse(success=False, msg='Not correct password.')
    await set_auth_cookies(response, user)
    return BaseResponse()


@auth_router.get('/exists', response_model=UserExistsResponse)
async def check_user_exists(request: Request, username: str) -> UserExistsResponse:
    userModel = UserModel(username=username)
    service = request.state.service
    if not await service.get_user(userModel):
        return UserExistsResponse(exists=False, username=username)
    return UserExistsResponse(exists=True, username=username)


@auth_router.post('/user', status_code=201)
async def register(
    request: Request, response: Response, data: UserRegisterData = Form()
) -> BaseResponse:
    user = UserModel(
        email=data.email,
        password=data.password,
        username=data.username,
        avatar=await data.avatar.read() if data.avatar else None,
        banner=await data.banner.read() if data.banner else None,
    )
    service = request.state.service
    user_id = await service.add_user(user)
    await set_auth_cookies(response, UserModel(id=user_id, username=data.username))
    return BaseResponse()
