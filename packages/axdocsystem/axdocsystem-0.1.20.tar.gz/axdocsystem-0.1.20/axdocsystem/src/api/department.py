from fastapi import APIRouter
from axdocsystem.db.schemas import DepartmentSchema
from axdocsystem.src.api.base_router import BaseAuthDependentRouter
from .base import BaseApi, with_uow, Request


class DepartmentApi(BaseApi):
    @with_uow
    async def create(self, req: Request, data: DepartmentSchema):
        await req.state.uow.repo.department.add(data)

    @with_uow
    async def update(self, req: Request, data: DepartmentSchema):
        await req.state.uow.repo.department.update(data)

    @with_uow
    async def delete(self, req: Request, id: int):
        await req.state.uow.repo.department.delete(id)

    @with_uow
    async def get(self, req: Request, id: int):
        return await req.state.uow.repo.department.get(id)

    @with_uow
    async def all(self, req: Request):
        return await req.state.uow.repo.department.all()

    def register_router(self, router: BaseAuthDependentRouter) -> APIRouter:
        router.post('/')(self.create)
        router.put('/')(self.update)
        router.delete('/{id}')(self.delete)
        router.get('/{id}', response_model=DepartmentSchema)(self.get)
        router.get('/', response_model=list[DepartmentSchema])(self.all)

        return router

