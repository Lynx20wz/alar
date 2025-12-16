from fastapi import APIRouter

from deps import comment_service_deps, auth_deps
from exceptions import CommentNotFound
from models import CommentModel
from schemas import BaseResponse, CommentCreateInfo, CommentInfo

comment_router = APIRouter(
    prefix='/comments',
    tags=['comments'],
)


@comment_router.get('/')
async def get_comments(service: comment_service_deps) -> list[CommentInfo]:
    return [CommentInfo.model_validate(comment) for comment in await service.get_all()]


@comment_router.get('/{comment_id}')
async def get_comment(service: comment_service_deps, comment_id: int) -> CommentInfo:
    comment = await service.get_comment(comment_id)

    if not comment:
        raise CommentNotFound()
    return CommentInfo.model_validate(comment)


@comment_router.post('/', tags=['Authorized'], dependencies=[auth_deps])
async def add_comment(
    service: comment_service_deps,
    comment: CommentCreateInfo,
) -> BaseResponse:
    new_comment = await service.add(CommentModel(**comment.model_dump()))
    return BaseResponse[int](data=new_comment.id)
