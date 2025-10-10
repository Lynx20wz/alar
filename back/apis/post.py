from fastapi import APIRouter, Depends

from back.deps import get_db_session
from back.schemas import PostCreateInfo, PostInfo, UserInfo, BaseResponse
from database import DataBaseCrud, PostModel
from deps import get_current_user, get_db_session
from jwt import JWTBearer

post_router = APIRouter(
    prefix='/post',
    tags=['post'],
)
db = DataBaseCrud()


@post_router.get('/')
async def get_posts(
    session=Depends(get_db_session), user: UserInfo | None = Depends(get_current_user)
) -> list[PostInfo]:
    return await db.get_posts(session, user.id if user else 0)


@post_router.get('/{post_id}')
async def get_post(
    post_id: int, session=Depends(get_db_session), user: UserInfo | None = Depends(get_current_user)
) -> PostInfo:
    post = await db.get_post(session, post_id, user.id if user else 0)
    if not post:
        raise PostNotFound()
    post.is_liked = post.is_liked_by(user.id if user else 0)
    return post


@post_router.post('/', dependencies=[Depends(JWTBearer())])
async def add_post(
    post: PostCreateInfo,
    session=Depends(get_db_session),
    user: UserInfo = Depends(get_current_user),
) -> BaseResponse:
    post_id = await db.add_post(session, PostModel(**post.model_dump(), author_id=user.id))
    return BaseResponse(detail={'post_id': post_id})
