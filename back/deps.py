__all__ = ('get_current_user', 'user_deps', 'ServiceFactory')

from typing import Annotated, AsyncGenerator

from fastapi import Depends, Request

from db import get_session
from repository import UserRepository
from schemas import UserInfo
from services import *


class ServiceFactory:
    def __init__(self, service_class: type[BaseService]):
        self.service_class = service_class

    async def __call__(self, request: Request) -> AsyncGenerator[BaseService, None]:
        service = self.service_class(await get_session())
        request.state.session = service
        yield service


async def get_current_user(request: Request) -> None:
    username = request.cookies.get('username')
    if not username:
        return
    user = await UserRepository(session=request.state.session).get_by(username=username)
    if not user:
        return
    else:
        request.state.user = UserInfo.model_validate(user)


user_deps = Annotated[None, Depends(get_current_user)]
