__all__ = ('ServiceFactory',)

from typing import Annotated, Any

from fastapi import Depends, Request

from db import get_session
from services import *


class ServiceFactory:
    def __init__(self, service_class: type[BaseService]):
        self.service_class = service_class

    async def __call__(
        self,
        request: Request,
        session=Depends(get_session),
    ) -> BaseService[Any]:
        service = self.service_class(session)
        request.state.service = service
        return service
