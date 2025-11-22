from fastapi import APIRouter, Depends, Request, Response

from deps import ServiceFactory, user_deps
from exceptions import PostNotFound
from jwt import JWTBearer
from models import LikePostModel, PostModel
from schemas import BaseResponse, PostCreateInfo, PostInfo
from services import PostService

post_router = APIRouter(
    prefix='/posts',
    tags=['post'],
    dependencies=[Depends(ServiceFactory(PostService))],
)


@post_router.get('/', response_model=list[PostInfo])
async def get_posts(request: Request, user: user_deps) -> list[PostModel]:
    return await request.state.service.get_posts(user.id if user else 0)


@post_router.get('/{post_id}', response_model=PostInfo)
async def get_post(post_id: int, request: Request, user: user_deps) -> PostModel:
    service = request.state.service
    post = await service.get(post_id)
    if not post:
        raise PostNotFound()
    post.is_liked = post.is_liked_by(user.id if user else 0)
    return post


@post_router.get('/{post_id}/image')
async def get_post_image(post_id: int, request: Request) -> Response:
    service = request.state.service
    post = await service.get(post_id)
    if not post or not post.image:
        raise PostNotFound()

    headers = {
        'Content-Type': 'image/png',
        'Content-Disposition': f'attachment; filename={post.id}_img.png',
    }

    return Response(content=post.image, media_type='image/png', headers=headers)


@post_router.post('/{post_id}/like', dependencies=[Depends(JWTBearer())])
async def like_post(request: Request, post_id: int) -> BaseResponse:
    service = request.state.session
    user = request.state.user
    post = await service.get_post(post_id)
    if not post:
        raise PostNotFound()
    if post.is_liked_by(user.id):
        await service.delete(LikePostModel(post_id=post_id, user_id=user.id))
    else:
        await service.add(LikePostModel(post_id=post_id, user_id=user.id))
    return BaseResponse[bool](
        data=not post.is_liked_by(user.id)
    )  # "not" because the status was changed to the opposite


@post_router.post('/', status_code=201, dependencies=[Depends(JWTBearer())])
async def add_post(
    request: Request,
    post: PostCreateInfo,
) -> BaseResponse:
    service = request.state.session
    user = request.state.user
    post_id = await service.add(PostModel(**post.model_dump(), author_id=user.id))
    return BaseResponse[int](data=post_id)
