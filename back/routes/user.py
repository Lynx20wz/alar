from fastapi import (
    APIRouter,
    Depends,
    File,
    Request,
    Response,
    UploadFile,
)

from exceptions import ImageNotFound, UserNotFound
from jwt import JWTBearer
from schemas import BaseResponse, FileResponse, UserInfo
from deps import user_service_deps

user_router = APIRouter(
    prefix='/users',
    tags=['user'],
)


@user_router.get(
    '/',
    tags=['Authorized'],
    dependencies=[Depends(JWTBearer())],
    responses={404: {'description': 'User not found'}},
)
async def get_me(request: Request) -> BaseResponse[UserInfo]:
    user = request.state.user

    if not user:
        raise UserNotFound()

    return BaseResponse[UserInfo](data=user)


@user_router.get('/{username}', responses={404: {'description': 'User not found'}})
async def get_user(service: user_service_deps, username: str) -> BaseResponse[UserInfo]:
    user = await service.get_user_by_username(username)
    return BaseResponse[UserInfo](data=UserInfo.model_validate(user))


@user_router.get('/avatar/{username}', responses={404: {'description': 'Image not found'}})
async def get_user_avatar(service: user_service_deps, username: str) -> Response:
    user = await service.get_user_by_username(username=username)

    if not user.avatar:
        raise ImageNotFound()

    return FileResponse(user.avatar, 'avatar.png')


@user_router.patch(
    '/avatar',
    tags=['Authorized'],
    dependencies=[Depends(JWTBearer())],
    responses={404: {'description': 'User not found'}},
)
async def set_user_avatar(
    service: user_service_deps, request: Request, file: UploadFile = File(...)
) -> BaseResponse:
    user = request.state.user

    await service.update(user.id, avatar=await file.read())
    return BaseResponse()


@user_router.get('/banner/{username}', responses={404: {'description': 'Image not found'}})
async def get_user_banner(service: user_service_deps, username: str) -> Response:
    user_db = await service.get_user_by_username(username)

    if not user_db.banner:
        raise ImageNotFound()

    return FileResponse(user_db.banner, 'banner.png')


@user_router.patch(
    '/banner',
    tags=['Authorized'],
    dependencies=[Depends(JWTBearer())],
    responses={404: {'description': 'User not found'}},
)
async def set_user_banner(
    service: user_service_deps, request: Request, file: UploadFile = File(...)
) -> BaseResponse:
    user = request.state.user
    await service.update(user.id, banner=await file.read())
    return BaseResponse()
