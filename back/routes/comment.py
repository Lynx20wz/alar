from fastapi import APIRouter, Depends, Request

from deps import ServiceFactory
from exceptions import CommentNotFound
from jwt import JWTBearer
from models import CommentModel
from schemas import BaseResponse, CommentInfoWithPost
from services import CommentService

comment_router = APIRouter(
    prefix='/comment',
    tags=['comment'],
    dependencies=[Depends(ServiceFactory(CommentService))],
)


@comment_router.get('/')
async def get_comments(request: Request) -> list[CommentInfoWithPost]:
    service = request.state.service
    
    return [
        CommentInfoWithPost.model_validate(comment)
        for comment in await service.get_all()
    ]


@comment_router.get('/{comment_id}')
async def get_comment(comment_id: int, request: Request) -> CommentInfoWithPost:
    service = request.state.service
    comment = await service.get_comment(comment_id)
    
    if not comment:
        raise CommentNotFound()
    return CommentInfoWithPost.model_validate(comment)


@comment_router.post('/', dependencies=[Depends(JWTBearer())])
async def add_comment(
    comment: CommentInfoWithPost,
    request: Request,
) -> BaseResponse:
    service = request.state.service
    user = request.state.user
    post = await service.get(comment.post.id)
    if not post:
        raise CommentNotFound()
    commentOBJ = service.add(CommentModel(**comment.model_dump(), author_id=user.id))
    return BaseResponse[int](data=commentOBJ)
