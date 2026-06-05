from abc import ABC
from typing import Any, Generic, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db import Base

ModelType = TypeVar('ModelType', bound=Base)


class BaseRepository(ABC, Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, id: int) -> ModelType | None:
        return await self.session.scalar(select(self.model).where(self.model.id == id))

    async def get_by(self, **kwargs: dict[str, Any]) -> ModelType | None:
        filters = [getattr(self.model, key) == value for key, value in kwargs.items()]

        if filters:
            return await self.session.scalar(select(self.model).where(*filters))

    async def get_by_model(self, model: ModelType) -> ModelType | None:
        filters = [getattr(self.model, key) == value for key, value in model.__dict__.items()]

        if filters:
            return await self.session.scalar(select(self.model).where(*filters))

    async def get_all(self, offset: int) -> list[ModelType]:
        result = await self.session.scalars(select(self.model).limit(10).offset(offset))
        return list(result.unique())

    async def update(self, obj: ModelType, **fields: dict[str, Any]) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id == obj.id)
            .values(**fields)
            .execution_options(synchronize_session='fetch')
        )

        _ = await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, obj: ModelType) -> None:
        _ = await self.session.execute(delete(self.model).where(self.model.id == obj.id))
        await self.session.commit()
