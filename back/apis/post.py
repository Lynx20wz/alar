from fastapi import APIRouter, Depends

from back.deps import get_db_session
from back.schemas import PostInfo, UserInfo
from database import DataBaseCrud
from deps import get_user, get_db_session

post_router = APIRouter(
    prefix='/post',
    tags=['post'],
)
db = DataBaseCrud()


@post_router.get('/')
async def get_posts(
    session=Depends(get_db_session), user: UserInfo = Depends(get_user)
) -> list[PostInfo]:
    return await db.get_posts(session, user.id)


@post_router.get('/{post_id}')
async def get_post(
    post_id: int, session=Depends(get_db_session), user: UserInfo = Depends(get_user)
) -> PostInfo:
    post = await db.get_post(session, post_id, user.id)
    if not post:    
        raise PostNotFound()
    return post


@post_router.post('/')
async def add_post(post, session=Depends(get_db_session)):
    return await db.add_post(session, post)
