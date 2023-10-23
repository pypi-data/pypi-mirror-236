from fastapi import APIRouter
from axdocsystem.db.schemas import OrganizationSchema
from axdocsystem.src.api.base_router import BaseAuthDependentRouter
from .base import BaseApi, with_uow, Request


class OrganizationApi(BaseApi):
    @with_uow
    async def create(self, req: Request, data: OrganizationSchema):
        await req.state.uow.repo.organization.add(data)

    @with_uow
    async def update(self, req: Request, data: OrganizationSchema):
        await req.state.uow.repo.organization.update(data)

    @with_uow
    async def delete(self, req: Request, id: int):
        await req.state.uow.repo.organization.delete(id)

    @with_uow
    async def get(self, req: Request, id: int):
        return await req.state.uow.repo.organization.get(id)

    @with_uow
    async def all(self, req: Request):
        return await req.state.uow.repo.organization.all()

    def register_router(self, router: BaseAuthDependentRouter) -> APIRouter:
        router.post('/')(self.create)
        router.put('/')(self.update)
        router.delete('/{id}')(self.delete)
        router.get('/{id}', response_model=OrganizationSchema)(self.get)
        router.get('/', response_model=list[OrganizationSchema])(self.all)

        return router

