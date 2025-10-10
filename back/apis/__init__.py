__all__ = ('all_routers', 'post_router', 'auth_router', 'user_router', 'comment_router')

from apis.post import post_router
from apis.auth import auth_router
from apis.user import user_router
from apis.comment import comment_router

all_routers = (post_router, auth_router, user_router, comment_router)
