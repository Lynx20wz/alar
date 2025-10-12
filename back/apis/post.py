from fastapi import APIRouter, Depends, Response

from database import DataBaseCrud, LikedPost, PostModel
from deps import AsyncSession, get_current_user, get_db_session
from exceptions import PostNotFound
from jwt import JWTBearer
from schemas import BaseResponse, PostCreateInfo, PostInfo, UserInfo

post_router = APIRouter(
    prefix='/posts',
    tags=['post'],
)
db = DataBaseCrud()


@post_router.get('/')
async def get_posts(
    session=Depends(get_db_session), user: UserInfo | None = Depends(get_current_user)
) -> list[PostInfo]:
    posts = await db.get_posts(session, user.id if user else 0)

    return [PostInfo.model_validate(post) for post in posts]


@post_router.get('/{post_id}')
async def get_post(
    post_id: int,
    session: AsyncSession = Depends(get_db_session),
    user: UserInfo | None = Depends(get_current_user),
) -> PostInfo:
    post = await db.get_post(session, post_id)
    if not post:
        raise PostNotFound()
    post.is_liked = post.is_liked_by(user.id if user else 0)
    return PostInfo.model_validate(post)


@post_router.get('/{post_id}/image')
async def get_post_image(post_id: int, session: AsyncSession = Depends(get_db_session)):
    post = await db.get_post(session, post_id)
    if not post or not post.image:
        raise PostNotFound()

    headers = {
        'Content-Type': 'image/png',
        'Content-Disposition': f'attachment; filename={post.id}_img.png',
    }

    return Response(content=post.image, media_type='image/png', headers=headers)


@post_router.post('/{post_id}/like', dependencies=[Depends(JWTBearer())])
async def like_post(
    post_id: int,
    session: AsyncSession = Depends(get_db_session),
    user: UserInfo = Depends(get_current_user),
) -> BaseResponse:
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
    session: AsyncSession = Depends(get_db_session),
    user: UserInfo = Depends(get_current_user),
) -> BaseResponse:
    post_id = await db.add_post(session, PostModel(**post.model_dump(), author_id=user.id))
    return BaseResponse[int](data=post_id)
