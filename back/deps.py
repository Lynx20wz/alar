__all__ = (
    'ServiceFactory',
    # Factories
    'user_service_factory',
    'post_service_factory',
    'comment_service_factory',
    # Deps
    'user_service_deps',
    'post_service_deps',
    'comment_service_deps',
)

from typing import Annotated, Generic, TypeVar

from fastapi import Depends

from db import get_session
from services import *

ServiceType = TypeVar('ServiceType', bound=BaseService)


class ServiceFactory(Generic[ServiceType]):
    def __init__(self, service_type: type[ServiceType]):
        self.service_type = service_type

    def __call__(self, session=Depends(get_session)) -> ServiceType:
        return self.service_type(session)


user_service_factory = ServiceFactory(UserService)
post_service_factory = ServiceFactory(PostService)
comment_service_factory = ServiceFactory(CommentService)

user_service_deps = Annotated[UserService, Depends(user_service_factory)]
post_service_deps = Annotated[PostService, Depends(post_service_factory)]
comment_service_deps = Annotated[CommentService, Depends(comment_service_factory)]
