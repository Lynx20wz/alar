__all__ = ('all_routers', 'post_router', 'auth_router', 'user_router', 'comment_router')

from .auth import auth_router
from .comment import comment_router
from .post import post_router
from .user import user_router

all_routers = (post_router, auth_router, user_router, comment_router)
