from fastapi import APIRouter, Depends

from exceptions import PostNotFound
from schemas import CommentInfo, CommentInfoWithPost, UserInfo, BaseResponse
from database import DataBaseCrud, PostModel
from deps import get_current_user, get_db_session
from jwt import JWTBearer

comment_router = APIRouter(
    prefix='/comment',
    tags=['comment'],
)
db = DataBaseCrud()

@comment_router.get('/')
async def get_comments(
    session=Depends(get_db_session), user: UserInfo | None = Depends(get_current_user)
) -> list[CommentInfo]:
    return await db.get_comments(session, user.id if user else 0)


@comment_router.get('/{comment_id}')
async def get_comment(
    comment_id: int, session=Depends(get_db_session), user: UserInfo | None = Depends(get_current_user)
) -> CommentInfo:
    comment = await db.get_comment(session, comment_id, user.id if user else 0)
    if not comment:
        raise PostNotFound()
    return comment


@comment_router.post('/', dependencies=[Depends(JWTBearer())])
async def add_comment(
    comment: CommentInfoWithPost,
    session=Depends(get_db_session),
    user: UserInfo = Depends(get_current_user),
) -> BaseResponse:
    post = await db.get_post(session, comment.post_id, user.id if user else 0)
    if not post:
        raise PostNotFound()
    comment_id = await db.add_comment(session, PostModel(**comment.model_dump(), author_id=user.id))
    return BaseResponse(detail={'comment_id': comment_id})