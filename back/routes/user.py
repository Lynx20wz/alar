from fastapi import APIRouter, Depends, File, HTTPException, Request, Response, UploadFile

from exceptions import ErrorResponse, UserNotFound
from jwt import JWTBearer
from models import UserModel
from schemas import BaseResponse, FileResponse, UserInfo

user_router = APIRouter(
    prefix='/users',
    tags=['user'],
)


@user_router.get('/', dependencies=[Depends(JWTBearer())])
async def get_me(request: Request) -> BaseResponse[UserInfo]:
    user = request.state.user
    if not user:
        raise UserNotFound()
    return BaseResponse[UserInfo](data=user)


@user_router.get('/{username}', responses={404: {'model': ErrorResponse}})
async def get_user(request: Request, username: str) -> BaseResponse[UserInfo]:
    service = request.state.service
    user = await service.get_by(username=username)

    if not user:
        raise UserNotFound()

    return BaseResponse[UserInfo](data=user)


@user_router.get('/avatar/{username}', responses={404: {'model': ErrorResponse}})
async def get_user_avatar(request: Request, username: str) -> Response:
    service = request.state.service
    user = await service.get_by(username=username)

    if not user:
        raise UserNotFound()

    if not user.avatar:
        raise HTTPException(status_code=404, detail='Avatar not found')

    return FileResponse(user.avatar, 'avatar.png')


@user_router.patch(
    '/avatar/{username}',
    dependencies=[Depends(JWTBearer())],
    responses={404: {'model': ErrorResponse}},
)
async def set_user_avatar(request: Request, file: UploadFile = File(...)) -> BaseResponse:
    service = request.state.service
    user = request.state.user
    await service.update(user.id, avatar=await file.read())
    return BaseResponse()


@user_router.get('/banner/{username}', responses={404: {'model': ErrorResponse}})
async def get_user_banner(request: Request, username: str) -> Response:
    service = request.state.service
    user_db = await service.get(UserModel(username=username))

    if not user_db:
        raise UserNotFound()

    if not user_db.banner:
        raise HTTPException(status_code=404, detail='Banner not found')

    return FileResponse(user_db.banner, 'banner.png')


@user_router.patch(
    '/banner/{username}',
    dependencies=[Depends(JWTBearer())],
    responses={404: {'model': ErrorResponse}},
)
async def set_user_banner(request: Request, file: UploadFile = File(...)) -> BaseResponse:
    service = request.state.service
    user = request.state.user
    await service.update(user.id, banner=await file.read())
    return BaseResponse()
