from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response

from database import DataBaseCrud
from exceptions import UserNotFound, ErrorResponse
from database.models import UserModel
from schemas import UserResponse, UserInfo
from deps import get_db_session

user_router = APIRouter(
    prefix='/user',
    tags=['user'],
)
db = DataBaseCrud()


@user_router.get('/{username}', responses={404: {'model': ErrorResponse}})
async def get_user(username: str, session=Depends(get_db_session)) -> UserResponse:
    try:
        user_db = await db.get_user(session, UserModel(username=username))
    except UserNotFound:
        raise UserNotFound()
    return UserResponse(user = user_db)

@user_router.get('/avatar/{username}', responses={404: {'model': ErrorResponse}})
async def get_user_avatar(username: str, session=Depends(get_db_session)):
    try:
        user_db = await db.get_user(session, UserModel(username=username))
    except UserNotFound:
        raise UserNotFound()

    if not user_db.avatar:
        raise HTTPException(status_code=404, detail='Avatar not found')

    headers = {
        'Content-Type': 'image/png',
        'Content-Disposition': f'attachment; filename={username}.png',
    }

    return Response(content=user_db.avatar, media_type='image/png', headers=headers)


@user_router.get('/banner/{username}', responses={404: {'model': ErrorResponse}})
async def get_user_banner(username: str, session=Depends(get_db_session)):
    try:
        user_db = await db.get_user(session, UserModel(username=username))
    except UserNotFound:
        raise UserNotFound()

    if not user_db.banner:
        raise HTTPException(status_code=404, detail='Banner not found')

    headers = {
        'Content-Type': 'image/png',
        'Content-Disposition': f'attachment; filename={username}.png',
    }

    return Response(content=user_db.banner, media_type='image/png', headers=headers)
