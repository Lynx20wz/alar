from abc import ABC
from typing import Generic, Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from db import Base
from repository import BaseRepository

RepositoryType = TypeVar('RepositoryType', bound=BaseRepository)
ModelType = TypeVar('ModelType', bound=Base)


class BaseService(Generic[RepositoryType]):
    repo: type[RepositoryType]

    def __init__(self, session: AsyncSession):
        self.repository = self.repo(session)

    async def add(self, obj: ModelType) -> ModelType:
        return await self.repository.add(obj)

    async def get(self, id: int) -> Optional[ModelType]:
        return await self.repository.get(id)

    async def get_by(self, **kwargs) -> Optional[ModelType]:
        return await self.repository.get_by(**kwargs)

    async def get_by_model(self, model: ModelType) -> Optional[ModelType]:
        return await self.repository.get_by_model(model)

    async def get_all(self, offset: int = 0) -> list[Optional[ModelType]]:
        return await self.repository.get_all(offset)

    async def update(self, id: int, **fields) -> None:
        if not fields:
            return
        return await self.repository.update(id, **fields)

    async def delete(self, obj: type[ModelType]) -> None:
        return await self.repository.delete(obj)
