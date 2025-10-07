from fastapi import APIRouter, Form, Depends, Response
from database import DataBaseCrud
from jwt import JWTBearer, jwt_generator

from exceptions import NotCorrectPassword, UserNotFound
from database.models import UserModel
from schemas import *
from deps import get_db_session, get_user


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


@auth_router.post('/token', dependencies=[Depends(JWTBearer())])
async def validate_token(user: UserInfo = Depends(get_user)):
    return {'detail': 'Access granted', 'user': UserShortInfo.model_validate(user)}


@auth_router.post('/login', response_model=UserTokenResponse)
async def login(response: Response, session=Depends(get_db_session), data: UserLoginData = Form()):
    userModel = UserModel(username=data.username, password=data.password)
    try:
        user = await db.get_user(session, userModel, True)
        if user:
            await set_auth_cookies(response, user)
            return UserTokenResponse(detail='Success')
    except NotCorrectPassword:
        return UserTokenResponse(
            success=False,
            detail='Not correct password',
        )
    except UserNotFound:
        return UserTokenResponse(
            success=False,
            detail='User not found.',
        )


@auth_router.get('/exists', response_model=UserExistsResponse)
async def check_user_exists(username: str, session=Depends(get_db_session)):
    userModel = UserModel(username=username)
    try:
        await db.get_user(session, userModel)
    except UserNotFound:
        return UserExistsResponse(exists=False, username=username)
    return UserExistsResponse(exists=True, username=username)


@auth_router.post('/user', status_code=201, response_model=UserTokenResponse)
async def register(
    response: Response, session=Depends(get_db_session), data: UserRegisterData = Form()
):
    user = UserModel(
        email=data.email,
        password=data.password,
        username=data.username,
        avatar=await data.avatar.read() if data.avatar else None,
        banner=await data.banner.read() if data.banner else None,
    )
    user_id = await db.add_user(session, user)
    await set_auth_cookies(response, UserModel(id=user_id, username=data.username))
    return UserTokenResponse()
