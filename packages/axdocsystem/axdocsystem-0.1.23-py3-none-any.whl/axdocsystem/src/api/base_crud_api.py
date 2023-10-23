from abc import abstractmethod
from typing import Type
from fastapi import APIRouter
from pydantic import BaseModel
from axdocsystem.db.schemas import OrganizationSchema
from axdocsystem.src.api.base_router import BaseAuthDependentRouter
from axsqlalchemy.repository import BaseRepository
from .base import BaseApi, with_uow, Request


class BaseCRUDApi(BaseApi):
    @property
    @abstractmethod
    def schema(self) -> Type[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    def get_repo(self, req: Request) -> BaseRepository:
        raise NotImplementedError

    @with_uow
    async def create(self, req: Request, data: OrganizationSchema):
        await self.get_repo(req).add(data)

    @with_uow
    async def update(self, req: Request, data: OrganizationSchema):
        await self.get_repo(req).update(data)

    @with_uow
    async def delete(self, req: Request, id: int):
        await self.get_repo(req).delete(id)

    @with_uow
    async def get(self, req: Request, id: int):
        return await self.get_repo(req).get(id)

    @with_uow
    async def all(self, req: Request):
        return await self.get_repo(req).all()

    def register_router(self, router: BaseAuthDependentRouter) -> APIRouter:
        router.post('/')(self.create)
        router.put('/')(self.update)
        router.delete('/{id}')(self.delete)
        router.get('/{id}', response_model=self.schema)(self.get)
        router.get('/', response_model=list[self.schema])(self.all)

        return router

