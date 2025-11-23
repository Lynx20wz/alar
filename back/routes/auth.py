from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Path, Request, Response

from deps import ServiceFactory
from exceptions import NotCorrectPassword, UserNotFound
from jwt import jwt_generator
from models import UserModel
from schemas import *
from services import UserService

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    dependencies=[Depends(ServiceFactory(UserService))],
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
    request: Request,
    response: Response,
    data: UserLoginData = Form(),
) -> BaseResponse:
    service: UserService = request.state.service

    try:
        user = await service.login(data.username, data.password)
    except UserNotFound:
        return BaseResponse(success=False, msg='User not found.')
    except NotCorrectPassword:
        return BaseResponse(success=False, msg='Not correct password.')

    await set_auth_cookies(response, user)
    return BaseResponse[UserModel](data=user)


@auth_router.get('/exists', response_model=UserExistsResponse)
async def check_user_exists(
    request: Request,   
    user_id: Annotated[Optional[int], Path(..., description='Have priority over username')] = None,
    username: Optional[str] = None,
) -> UserExistsResponse:
    if not user_id and not username:
        raise HTTPException(status_code=422, detail='user_id or username must be provided')

    service: UserService = request.state.service

    user_id, username = await service.get_base_info(user_id, username)

    if user_id:
        return UserExistsResponse(user_id=user_id, username=username, exists=True)
    else:
        return UserExistsResponse(exists=False)


@auth_router.post('/user', status_code=201)
async def register(
    request: Request, response: Response, data: UserRegisterData = Form()
) -> BaseResponse:
    service: UserService = request.state.service
    user = await service.add_user(data)

    await set_auth_cookies(response, UserModel(id=user.id, username=user.username))
    return BaseResponse[UserModel](data=user)
