import enum
import sqlalchemy as sa
from axsqlalchemy.model import BaseTableInt, BaseTable, Base


__all__ = [
    'Base',
    'Organization',
]


class DocumentStatusEnum(enum.Enum):
    NEW = 'new'
    SUCCESS = 'success'


class UsersPosition(enum.Enum):
    STUDENT = 1
    PROFESSOR = 2
    ADMINISTRATOR = 3
    LIBRARIAN = 4
    RESEARCHER = 5
    DEAN = 6
    CHAIRPERSON = 7
    JANITOR = 8



class Organization(BaseTableInt):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.String)


class Department(BaseTableInt):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    organization_id = sa.Column(sa.ForeignKey(Organization.id))


class Users(BaseTable):
    email = sa.Column(sa.String(255), primary_key=True)
    fullname = sa.Column(sa.String(255), nullable=False)
    department_id = sa.Column(sa.ForeignKey(Department.id))
    type = sa.Column(sa.Enum(UsersPosition))
    phone = sa.Column(sa.String(255), nullable=False)
    password_hash = sa.Column(sa.String(255))


class Document(BaseTableInt):
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(255))
    sender_id = sa.Column(sa.ForeignKey(Users.email))
    executor_id = sa.Column(sa.ForeignKey(Users.email))
    file_name = sa.Column(sa.String(255))
    description = sa.Column(sa.String)
    from_id = sa.Column(sa.Integer)
    to_id = sa.Column(sa.Integer)
    status = sa.Column(sa.Enum(DocumentStatusEnum))
    from_org_id = sa.Column(sa.ForeignKey(Organization.id))
    to_org_id = sa.Column(sa.ForeignKey(Organization.id))
    send_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    received_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    expiring_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

