from pydantic import BaseSettings
from axsqlalchemy.settings import Settings as _DBSettings


class JWTSettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int


class Settings(_DBSettings, JWTSettings):
    class Config:
        env_file = '.env'


