__all__ = (
    'all_routers',
    'post_router',
    'auth_router',
    'user_router',
    'comment_router',
    'v1_router',
)

from fastapi import APIRouter

from .auth import auth_router
from .comment import comment_router
from .post import post_router
from .user import user_router

all_routers = (post_router, auth_router, user_router, comment_router)

v1_router = APIRouter(prefix='/v1')

for router in all_routers:
    v1_router.include_router(router)
