from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile

from database import DataBaseCrud
from database.models import UserModel
from deps import get_current_user, get_db_session
from exceptions import ErrorResponse, UserNotFound
from jwt import JWTBearer
from schemas import BaseResponse, FileResponse, UserInfo, UserResponse

user_router = APIRouter(
    prefix='/users',
    tags=['user'],
)
db = DataBaseCrud()


@user_router.get('/', dependencies=[Depends(JWTBearer())])
async def get_me(user=Depends(get_current_user)) -> UserResponse:
    if not user:
        raise UserNotFound()
    return UserResponse(user=user)


@user_router.get('/{username}', responses={404: {'model': ErrorResponse}})
async def get_user(username: str, session=Depends(get_db_session)) -> UserResponse:
    if not (user_db := await db.get_user(session, UserModel(username=username))):
        raise UserNotFound()
    return UserResponse(user=UserInfo.model_validate(user_db))


@user_router.get('/avatar/{username}', responses={404: {'model': ErrorResponse}})
async def get_user_avatar(username: str, session=Depends(get_db_session)) -> Response:
    if not (user_db := await db.get_user(session, UserModel(username=username))):
        raise UserNotFound()

    if not user_db.avatar:
        raise HTTPException(status_code=404, detail='Avatar not found')

    return FileResponse(user_db.avatar, 'avatar.png')


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
async def get_user_banner(username: str, session=Depends(get_db_session)) -> Response:
    user_db = await db.get_user(session, UserModel(username=username))

    if not user_db:
        raise UserNotFound()

    if not user_db.banner:
        raise HTTPException(status_code=404, detail='Banner not found')

    return FileResponse(user_db.banner, 'banner.png')


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
