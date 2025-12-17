from typing import Generic, Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from db import Base
from exceptions import NotFoundError
from repository import BaseRepository

RepositoryType = TypeVar('RepositoryType', bound=BaseRepository)
ModelType = TypeVar('ModelType', bound=Base)


class BaseService(Generic[RepositoryType, ModelType]):
    repo: type[RepositoryType]

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = self.repo(session)

    async def _get_or_raise(self, obj: ModelType | None) -> ModelType:
        if not obj:
            raise NotFoundError()
        return obj

    async def add(self, obj: ModelType) -> ModelType:
        return await self.repository.add(obj)

    async def get(self, obj_id: int) -> Optional[ModelType]:
        return await self.repository.get(obj_id)

    async def get_by(self, **kwargs) -> Optional[ModelType]:
        return await self.repository.get_by(**kwargs)

    async def get_by_model(self, model: ModelType) -> Optional[ModelType]:
        return await self.repository.get_by_model(model)

    async def get_all(self, offset: int = 0) -> list[Optional[ModelType]]:
        return await self.repository.get_all(offset)

    async def update(self, obj_id: int, **fields) -> None:
        obj = await self.get(obj_id)

        if not obj:
            raise NotFoundError
        if not fields:
            raise ValueError('No fields to update')

        return await self.repository.update(obj, **fields)

    async def delete(self, obj: type[ModelType]) -> None:
        return await self.repository.delete(obj)
