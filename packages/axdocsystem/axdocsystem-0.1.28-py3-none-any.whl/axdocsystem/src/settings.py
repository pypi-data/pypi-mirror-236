from axsqlalchemy.settings import Settings as DBSettings
from axdocsystem.utils.settings import (
    AuthRouteSettings as AuthSettings,
    LimitationSettings as LimitSettings,
)


class Settings(DBSettings, AuthSettings, LimitSettings):
    class Config:
        env_file = '.env'


