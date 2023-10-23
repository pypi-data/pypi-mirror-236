from fastapi import FastAPI

from axdocsystem.src.settings import Settings
from .base_router import TUOWFactory
from .organization import OrganizationApi
from .department import DepartmentApi
from .users import UsersApi
from .document import DocumentApi


def register_all(app: FastAPI, uowf: TUOWFactory, settings: Settings) -> FastAPI:
    app.include_router(OrganizationApi(uowf, settings).router, tags=['Organization'], prefix='/api/organization')
    app.include_router(DepartmentApi(uowf, settings).router, tags=['Department'], prefix='/api/department')
    app.include_router(UsersApi(uowf, settings).router, tags=['Users'], prefix='/api/users')
    app.include_router(DocumentApi(uowf, settings).router, tags=['Document'], prefix='/api/document')
    
    return app


