from typing import Optional

from pydantic import BaseModel, EmailStr

from ..core.schemas.base import MainSchema


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


class UserShowSchema(MainSchema):
    id: int
    email: EmailStr
    is_active: bool

class TokenVerifyOrRefreshSchema(BaseModel):
    token: str


class JWTTokensData(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenData(BaseModel):
    access_token: str
