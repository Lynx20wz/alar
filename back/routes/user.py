from typing import Annotated

from fastapi import (
    APIRouter,
    File,
    Query,
    Response,
    UploadFile,
)

from deps import auth_deps, user_deps, user_service_deps
from exceptions import ImageNotFound
from schemas import BaseResponse, FileResponse, UserInfo

user_router = APIRouter(
    prefix='/users',
    tags=['user'],
)


@user_router.get('', responses={404: {'description': 'User not found'}})
async def get_user(
    service: user_service_deps,
    username: Annotated[str, Query(description='The username to get a user for', alias='u')],
) -> BaseResponse[UserInfo]:
    user = await service.get_user_by_username(username)
    return BaseResponse[UserInfo](data=UserInfo.model_validate(user))


@user_router.get(
    '/',  # TODO think about it later
    tags=['Authorized'],
    dependencies=[auth_deps],
)
async def get_me(user: user_deps) -> BaseResponse[UserInfo]:
    return BaseResponse[UserInfo](data=UserInfo.model_validate(user))


@user_router.get('/avatar', responses={404: {'description': 'Image not found'}})
async def get_user_avatar(
    service: user_service_deps,
    username: Annotated[str, Query(description='The username to get an avatar for', alias='u')],
) -> Response:
    user = await service.get_user_by_username(username=username)

    if not user.avatar:
        raise ImageNotFound()

    return FileResponse(user.avatar, 'avatar.png')


@user_router.patch(
    '/avatar',
    tags=['Authorized'],
    dependencies=[auth_deps],
    responses={404: {'description': 'User not found'}},
)
async def set_user_avatar(
    service: user_service_deps, user: user_deps, file: UploadFile = File(...)
) -> BaseResponse:
    await service.update(user.id, avatar=await file.read())
    return BaseResponse()


@user_router.get('/banner', responses={404: {'description': 'Image not found'}})
async def get_user_banner(
    service: user_service_deps,
    username: Annotated[str, Query(description='The username to get an banner for', alias='u')],
) -> Response:
    user_db = await service.get_user_by_username(username)

    if not user_db.banner:
        raise ImageNotFound()

    return FileResponse(user_db.banner, 'banner.png')


@user_router.patch(
    '/banner',
    tags=['Authorized'],
    dependencies=[auth_deps],
    responses={404: {'description': 'User not found'}},
)
async def set_user_banner(
    service: user_service_deps, user: user_deps, file: UploadFile = File(...)
) -> BaseResponse:
    await service.update(user.id, banner=await file.read())
    return BaseResponse()
