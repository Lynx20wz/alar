from fastapi import APIRouter, Depends

from exceptions import CommentNotFound
from schemas import CommentInfoWithPost, UserInfo, BaseResponse
from database import DataBaseCrud, CommentModel
from deps import get_current_user, get_db_session
from jwt import JWTBearer

comment_router = APIRouter(
    prefix='/comment',
    tags=['comment'],
)
db = DataBaseCrud()


@comment_router.get('/')
async def get_comments(session=Depends(get_db_session)) -> list[CommentInfoWithPost]:
    return [CommentInfoWithPost.model_validate(comment) for comment in await db.get_comments(session)]


@comment_router.get('/{comment_id}')
async def get_comment(comment_id: int, session=Depends(get_db_session)) -> CommentInfoWithPost:
    comment = await db.get_comment(session, comment_id)
    if not comment:
        raise CommentNotFound()
    return CommentInfoWithPost.model_validate(comment)


@comment_router.post('/', dependencies=[Depends(JWTBearer())])
async def add_comment(
    comment: CommentInfoWithPost,
    session=Depends(get_db_session),
    user: UserInfo = Depends(get_current_user),
) -> BaseResponse:
    post = await db.get_post(session, comment.post.id)
    if not post:
        raise CommentNotFound()
    comment_id = await db.add_comment(session, CommentModel(**comment.model_dump(), author_id=user.id))
    return BaseResponse[int](data=comment_id)
