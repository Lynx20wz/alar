from typing import Annotated

from fastapi import APIRouter, Query

from deps import auth_deps, comment_service_deps, user_deps
from exceptions import CommentNotFound
from models import CommentModel
from schemas import BaseResponse, CommentCreateInfo, CommentInfo

comment_router = APIRouter(
    prefix='/comments',
    tags=['comments'],
)


@comment_router.get('')
async def get_comments(service: comment_service_deps) -> list[CommentInfo]:
    return [CommentInfo.model_validate(comment) for comment in await service.get_all()]


@comment_router.get('')
async def get_comment(
    service: comment_service_deps, comment_id: Annotated[int, Query(alias='c')]
) -> CommentInfo:
    comment = await service.get_comment(comment_id)

    if not comment:
        raise CommentNotFound()
    return CommentInfo.model_validate(comment)


@comment_router.post('', tags=['Authorized'], dependencies=[auth_deps], response_model=CommentInfo)
async def add_comment(
    service: comment_service_deps,
    user: user_deps,
    comment_info: CommentCreateInfo,
) -> CommentModel:
    return await service.add(
        CommentModel(
            content=comment_info.content,
            post_id=comment_info.post_id,
            author_id=user.id,
        )
    )
