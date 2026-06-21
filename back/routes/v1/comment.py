from fastapi import APIRouter

from deps import comment_service_deps, user_deps
from exceptions import CommentNotFound
from models import CommentModel
from schemas import CommentCreateSchema, CommentReadSchema

comment_router = APIRouter(
    prefix='/comments',
    tags=['comments'],
)


@comment_router.get('/{comment_id}')
async def get_comment(service: comment_service_deps, comment_id: int) -> CommentReadSchema:
    comment = await service.get_comment(comment_id)

    if not comment:
        raise CommentNotFound()
    return CommentReadSchema.model_validate(comment)


@comment_router.post('', tags=['Authorized'])
async def add_comment(
    service: comment_service_deps,
    user: user_deps,
    comment_info: CommentCreateSchema,
) -> CommentReadSchema:
    comment = CommentModel(
        content=comment_info.content,
        post_id=comment_info.post_id,
        author_id=user.id,
    )
    return CommentReadSchema.model_validate(await service.add(comment))
