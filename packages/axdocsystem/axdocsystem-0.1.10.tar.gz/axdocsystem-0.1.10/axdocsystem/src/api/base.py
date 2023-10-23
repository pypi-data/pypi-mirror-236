from abc import ABC, abstractmethod
from typing import Union
from fastapi import APIRouter, Request as _Request
from functools import wraps

from db.schemas import Admin
from settings import JWTSettings
from .base_auth_dependent_router import BaseAuthDependentRouter, TUOWFactory, TUOW


class State:
    uow: TUOW
    admin: Admin 


class Request(_Request):
    state: State


class BaseRouter(ABC):
    def __init__(self, uowf: TUOWFactory, settings: JWTSettings,  router: Union[BaseAuthDependentRouter, None] = None) -> None:
        self.router = router or BaseAuthDependentRouter(uowf=uowf, settings=settings)
        self.register_router(self.router)
        self.uowf = uowf

    @abstractmethod
    def register_router(self, router: APIRouter) -> APIRouter:
        pass


def with_uow(f):
    @wraps(f)
    async def wrapper(self: BaseRouter, *args, req: Request, **kwargs):
        async with self.uowf() as uow:
            req.state.uow = uow
            return await f(self, *args, req=req, **kwargs)
    
    return wrapper


