from fastapi import APIRouter, Depends, Request, Response

from deps import post_service_deps
from exceptions import ImageNotFound
from jwt import JWTBearer
from models import PostModel
from schemas import BaseResponse, PostCreateInfo, PostInfo

post_router = APIRouter(
    prefix='/posts',
    tags=['post'],
)


@post_router.get('/', response_model=list[PostInfo])
async def get_posts(service: post_service_deps) -> list[PostModel]:
    return await service.get_posts()


@post_router.get('/{post_id}', response_model=PostInfo)
async def get_post(service: post_service_deps, post_id: int, user_id: int = 0) -> PostModel:
    return await service.get_post(post_id, user_id)


@post_router.get('/{post_id}/image')
async def get_post_image(service: post_service_deps, post_id: int) -> Response:
    post = await service.get_post(post_id)
    if not post.image:
        raise ImageNotFound()

    headers = {
        'Content-Type': 'image/png',
        'Content-Disposition': f'attachment; filename={post.id}_img.png',
    }

    return Response(content=post.image, media_type='image/png', headers=headers)


@post_router.post('/{post_id}/like', tags=['Authorized'], dependencies=[Depends(JWTBearer())])
async def like_post(service: post_service_deps, request: Request, post_id: int) -> BaseResponse:
    user = request.state.user
    current_status = await service.change_like_status(post_id, user.id)
    return BaseResponse[bool](data=current_status)


@post_router.post('/', status_code=201, tags=['Authorized'], dependencies=[Depends(JWTBearer())])
async def add_post(
    service: post_service_deps,
    request: Request,
    post: PostCreateInfo,
) -> BaseResponse:
    user = request.state.user

    post_id = await service.add(PostModel(**post.model_dump(), author_id=user.id))
    return BaseResponse[int](data=post_id.id)
