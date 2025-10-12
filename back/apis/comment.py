from fastapi import APIRouter, Depends

from database import CommentModel, DataBaseCrud
from deps import user_deps, session_deps
from exceptions import CommentNotFound
from jwt import JWTBearer
from schemas import BaseResponse, CommentInfoWithPost

comment_router = APIRouter(
    prefix='/comment',
    tags=['comment'],
)
db = DataBaseCrud()


@comment_router.get('/')
async def get_comments(session: session_deps) -> list[CommentInfoWithPost]:
    return [
        CommentInfoWithPost.model_validate(comment) for comment in await db.get_comments(session)
    ]


@comment_router.get('/{comment_id}')
async def get_comment(comment_id: int, session: session_deps) -> CommentInfoWithPost:
    comment = await db.get_comment(session, comment_id)
    if not comment:
        raise CommentNotFound()
    return CommentInfoWithPost.model_validate(comment)


@comment_router.post('/', dependencies=[Depends(JWTBearer())])
async def add_comment(
    comment: CommentInfoWithPost,
    session: session_deps,
    user: user_deps,
) -> BaseResponse:
    post = await db.get_post(session, comment.post.id)
    if not post:
        raise CommentNotFound()
    comment_id = await db.add_comment(
        session, CommentModel(**comment.model_dump(), author_id=user.id)
    )
    return BaseResponse[int](data=comment_id)
