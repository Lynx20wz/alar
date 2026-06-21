from typing import Annotated

from fastapi import APIRouter, Query, Response

from deps import optional_user_deps, post_service_deps, user_deps
from exceptions import ImageNotFound, PostNotFound
from models import PostModel
from schemas import PostCreateSchema, PostReadSchema

post_router = APIRouter(
    prefix='/posts',
    tags=['post'],
)


@post_router.get('/')
async def get_posts(service: post_service_deps, user: optional_user_deps) -> list[PostReadSchema]:
    return [
        PostReadSchema.model_validate(post)
        for post in await service.get_posts(user_id=user.id if user else None)
    ]


@post_router.get('/{post_id}')
async def get_post(
    service: post_service_deps,
    user: optional_user_deps,
    post_id: int,
) -> PostReadSchema:
    post = await service.get_post(post_id, user.id if user else None)
    if not post:
        raise PostNotFound(object_id=post_id)

    return PostReadSchema.model_validate(post)


@post_router.get('/image')
async def get_post_image(
    service: post_service_deps,
    post_id: Annotated[int, Query(description='The post ID to get an image for')],
) -> Response:
    post = await service.get_post(post_id)

    if not post:
        raise PostNotFound(object_id=post_id)

    if not post.image:
        raise ImageNotFound()

    headers = {
        'Content-Type': 'image/png',
        'Content-Disposition': f'attachment; filename={post.id}_img.png',
    }

    return Response(content=post.image, media_type='image/png', headers=headers)


@post_router.post('/{post_id}/like', tags=['Authorized'])
async def like_post(
    service: post_service_deps,
    user: user_deps,
    post_id: int,
) -> bool:
    current_status = await service.change_like_status(post_id, user.id)
    return current_status


@post_router.post(
    '/',
    status_code=201,
    tags=['Authorized'],
)
async def add_post(
    service: post_service_deps,
    user: user_deps,
    post_info: PostCreateSchema,
) -> Response:
    if await service.add(PostModel(**post_info.model_dump(), author_id=user.id)):
        return Response(status_code=201)
    return Response(status_code=500)
