from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Request
from fastapi.responses import Response

from back.database.core import Base
from database import DataBaseCrud
from exceptions import UserNotFound, ErrorResponse
from database.models import UserModel
from schemas import UserResponse, BaseResponse
from deps import get_db_session, get_current_user
from jwt import JWTBearer

user_router = APIRouter(
    prefix='/user',
    tags=['user'],
)
db = DataBaseCrud()

@user_router.get('/', dependencies=[Depends(JWTBearer())])
async def get_me(user=Depends(get_current_user)):
    if not user:
        raise UserNotFound()
    return UserResponse(user=user)

@user_router.get('/{username}', responses={404: {'model': ErrorResponse}})
async def get_user(username: str, session=Depends(get_db_session)) -> UserResponse:
    if not (user_db := await db.get_user(session, UserModel(username=username))):
        raise UserNotFound()
    return UserResponse(user=user_db)


@user_router.get('/avatar/{username}', responses={404: {'model': ErrorResponse}})
async def get_user_avatar(username: str, session=Depends(get_db_session)):
    if not (user_db := await db.get_user(session, UserModel(username=username))):
        raise UserNotFound()

    if not user_db.avatar:
        raise HTTPException(status_code=404, detail='Avatar not found')

    headers = {
        'Content-Type': 'image/png',
        'Content-Disposition': f'attachment; filename={username}.png',
    }

    return Response(content=user_db.avatar, media_type='image/png', headers=headers)


@user_router.post(
    '/avatar/{username}',
    dependencies=[Depends(JWTBearer())],
    responses={404: {'model': ErrorResponse}},
)
async def set_user_avatar(
    session=Depends(get_db_session), user=Depends(get_current_user), file: UploadFile = File(...)
) -> BaseResponse:
    await db.update_user(session, user.id, avatar=await file.read())
    return BaseResponse()


@user_router.get('/banner/{username}', responses={404: {'model': ErrorResponse}})
async def get_user_banner(username: str, session=Depends(get_db_session)):
    user_db = await db.get_user(session, UserModel(username=username))

    if not user_db:
        raise UserNotFound()

    if not user_db.banner:
        raise HTTPException(status_code=404, detail='Banner not found')

    headers = {
        'Content-Type': 'image/png',
        'Content-Disposition': f'attachment; filename={username}.png',
    }

    return Response(content=user_db.banner, media_type='image/png', headers=headers)


@user_router.post(
    '/banner/{username}',
    dependencies=[Depends(JWTBearer())],
    responses={404: {'model': ErrorResponse}},
)
async def set_user_banner(
    session=Depends(get_db_session), user=Depends(get_current_user), file: UploadFile = File(...)
) -> BaseResponse:
    await db.update_user(session, user.id, banner=await file.read())
    return BaseResponse()
