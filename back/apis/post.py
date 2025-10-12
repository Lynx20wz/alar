from fastapi import APIRouter, Depends, Response

from database import DataBaseCrud, LikedPost, PostModel
from deps import session_deps, user_deps
from exceptions import PostNotFound
from jwt import JWTBearer
from schemas import BaseResponse, PostCreateInfo, PostInfo

post_router = APIRouter(
    prefix='/posts',
    tags=['post'],
)
db = DataBaseCrud()


@post_router.get('/', response_model=list[PostInfo])
async def get_posts(session: session_deps, user: user_deps) -> list[PostModel]:
    return await db.get_posts(session, user.id if user else 0)


@post_router.get('/{post_id}', response_model=PostInfo)
async def get_post(post_id: int, session: session_deps, user: user_deps) -> PostModel:
    post = await db.get_post(session, post_id)
    if not post:
        raise PostNotFound()
    post.is_liked = post.is_liked_by(user.id if user else 0)
    return post


@post_router.get('/{post_id}/image')
async def get_post_image(post_id: int, session: session_deps) -> Response:
    post = await db.get_post(session, post_id)
    if not post or not post.image:
        raise PostNotFound()

    headers = {
        'Content-Type': 'image/png',
        'Content-Disposition': f'attachment; filename={post.id}_img.png',
    }

    return Response(content=post.image, media_type='image/png', headers=headers)


@post_router.post('/{post_id}/like', dependencies=[Depends(JWTBearer())])
async def like_post(post_id: int, session: session_deps, user: user_deps) -> BaseResponse:
    post = await db.get_post(session, post_id)
    if not post:
        raise PostNotFound()
    if post.is_liked_by(user.id):
        await db.remove_like(session, LikedPost(post_id=post_id, user_id=user.id))
    else:
        await db.add_like(session, LikedPost(post_id=post_id, user_id=user.id))
    return BaseResponse[bool](
        data=not post.is_liked_by(user.id)
    )  # "not" because the status was changed to the opposite


@post_router.post('/', status_code=201, dependencies=[Depends(JWTBearer())])
async def add_post(
    post: PostCreateInfo,
    session: session_deps,
    user: user_deps,
) -> BaseResponse:
    post_id = await db.add_post(session, PostModel(**post.model_dump(), author_id=user.id))
    return BaseResponse[int](data=post_id)
