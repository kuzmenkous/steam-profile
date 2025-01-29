from functools import lru_cache

from typing import Annotated

from pydantic import Field, field_validator, PostgresDsn, ValidationInfo
from pydantic_settings import BaseSettings, NoDecode

from .helpers import DotenvListHelper, load_environment


class AppSettings(BaseSettings):
    debug: bool = True
    name: str = "Steam Profile API"
    version: int = 1
    secret_key: str
    domain: str = "localhost:8000"
    protocol: str = "http"

    class Config:
        env_prefix = "app_"

    @property
    def base_url(self):
        return f"{self.protocol}://{self.domain}"

    @property
    def base_url_with_prefix(self):
        return f"{self.base_url}/id"


class PaginationSettings(BaseSettings):
    limit_per_page: int = 100

    class Config:
        env_prefix = "pagination_"


class JWTSettings(BaseSettings):
    access_token_expire: int
    refresh_token_expire: int
    algorithm: str

    class Config:
        env_prefix = "jwt_"


class CorsSettings(BaseSettings):
    origins: Annotated[list[str], NoDecode]

    class Config:
        env_prefix = "cors_"

    @field_validator("origins", mode="before")
    @classmethod
    def decode_origins(cls, v: list[str]) -> list[str]:
        return DotenvListHelper.get_list_from_value(v)


class StaticFilesSettings(BaseSettings):
    directory: str = "static"
    max_file_size: int = 10485760
    allowed_extensions: Annotated[list[str], NoDecode]

    class Config:
        env_prefix = "static_"

    @field_validator("allowed_extensions", mode="before")
    @classmethod
    def decode_allowed_extensions(cls, v: list[str]) -> list[str]:
        return DotenvListHelper.get_list_from_value(v)


class DBSettings(BaseSettings):
    name: str = Field(alias="db_name")
    user: str = Field(alias="db_user")
    password: str = Field(alias="db_password")
    host: str = Field(alias="db_host")
    port: int = Field(alias="db_port")
    scheme: str = Field(alias="db_scheme")
    url: str | None = Field(alias="db_url", default=None)

    @field_validator("url")
    @classmethod
    def assemble_db_url(cls, v: str | None, validation_info: ValidationInfo) -> str:
        if v is not None:
            return v
        values = validation_info.data
        url = PostgresDsn.build(
            scheme=values["scheme"],
            username=values["user"],
            password=values["password"],
            host=values["host"],
            port=values["port"],
            path=values["name"],
        )
        return str(url)


class RedisSettings(BaseSettings):
    url: str

    class Config:
        env_prefix = "redis_"


class Settings(BaseSettings):
    # App settings
    app: AppSettings = Field(default_factory=AppSettings)
    # Pagination settings
    pagination: PaginationSettings = Field(default_factory=PaginationSettings)
    # JWT settings
    jwt: JWTSettings = Field(default_factory=JWTSettings)
    # CORS settings
    cors: CorsSettings = Field(default_factory=CorsSettings)
    # Static files settings
    static: StaticFilesSettings = Field(default_factory=StaticFilesSettings)
    # Database settings
    db: DBSettings = Field(default_factory=DBSettings)
    # Redis settings
    redis: RedisSettings = Field(default_factory=RedisSettings)


@lru_cache
def get_settings() -> Settings:
    load_environment()
    return Settings()


settings = get_settings()
