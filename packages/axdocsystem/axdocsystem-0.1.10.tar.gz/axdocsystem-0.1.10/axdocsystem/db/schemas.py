from datetime import datetime
from typing import Optional
from axsqlalchemy.schema import BaseModel

from .enums import UsersPositionEnum, DocumentStatusEnum


class OrganizationSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]


class DepartmentSchema(BaseModel):
    id: int
    name: str
    organization_id: int


class UsersSchema(BaseModel):
    email: str
    fullname: str
    department_id: int
    position: UsersPositionEnum
    phone: str
    password_hash: str


class DocumentSchema(BaseModel):
    id: int
    title: str
    sender_id: str
    executor_id: str
    file_name: str
    description: Optional[str]
    from_id: int
    to_id: int
    status: DocumentStatusEnum
    from_org_id: int
    to_org_id: int
    send_at: datetime
    received_at: datetime
    expiring_at: datetime

