import io
from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    Response,
    UploadFile,
)
from fastapi.responses import StreamingResponse

from deps import user_deps, user_service_deps
from exceptions import ImageNotFound, UserNotFound
from schemas import *

user_router = APIRouter(
    prefix='/users',
    tags=['user'],
)


@user_router.get(
    '/me',
    tags=['Authorized'],
)
async def get_me(user: user_deps) -> UserReadSchema:
    return UserReadSchema.model_validate(user)


@user_router.get('/', responses={404: {'description': 'User not found'}})
async def get_user(
    service: user_service_deps,
    user_id: Annotated[int | None, Query(description='The user ID to get', alias='id')] = None,
    username: Annotated[str | None, Query(description='The username to get', alias='u')] = None,
) -> UserReadSchema:
    if user_id:
        user = await service.get_user_by_id(user_id)
    elif username:
        user = await service.get_user_by_username(username)
    else:
        raise HTTPException(400, 'Provide user_id or username')
    return UserReadSchema.model_validate(user)


@user_router.get('/avatar', responses={404: {'description': 'Image not found'}})
async def get_user_avatar(
    service: user_service_deps,
    user_id: Annotated[int, Query(description='The user ID to get an avatar for', alias='id')],
) -> Response:
    user = await service.get_user_by_id(user_id)

    if not user:
        raise UserNotFound(object_id=user_id)

    if not user.avatar:
        raise ImageNotFound()

    return StreamingResponse(io.BytesIO(user.avatar), media_type='image/png')


@user_router.patch(
    '/avatar',
    tags=['Authorized'],
    responses={404: {'description': 'User not found'}},
)
async def set_user_avatar(service: user_service_deps, user: user_deps, file: UploadFile):
    await service.update(user.id, avatar=await file.read())
    return Response(status_code=200)


@user_router.get('/banner', responses={404: {'description': 'Image not found'}})
async def get_user_banner(
    service: user_service_deps,
    user_id: Annotated[int, Query(description='The user ID to get an banner for', alias='id')],
) -> Response:
    user_db = await service.get_user_by_id(user_id)

    if not user_db:
        raise UserNotFound(object_id=user_id)

    if not user_db.banner:
        raise ImageNotFound()

    return StreamingResponse(io.BytesIO(user_db.banner), media_type='image/png')


@user_router.patch(
    '/banner',
    tags=['Authorized'],
    responses={404: {'description': 'User not found'}},
)
async def set_user_banner(service: user_service_deps, user: user_deps, file: UploadFile):
    await service.update(user.id, banner=await file.read())
    return Response(status_code=200)
