from fastapi import APIRouter, status

from ..core.db.dependencies import uowDEP

from .schemas import (
    UserCreateSchema,
    UserUpdateSchema,
    UserShowSchema,
    JWTTokensData,
    AccessTokenData,
    TokenVerifyOrRefreshSchema,
    LoginUserSchema,
)
from .service import UserService


router = APIRouter(
    prefix="/user",
)


@router.post(
    "/create/", response_model=UserShowSchema, status_code=status.HTTP_201_CREATED, tags=["user"]
)
async def create_user(uow: uowDEP, data: UserCreateSchema):
    return await UserService(uow).create_user(data)


@router.put("/update/{user_id}/", response_model=UserShowSchema, tags=["user"])
async def update_user(uow: uowDEP, user_id: int, data: UserUpdateSchema):
    return await UserService(uow).update_user(user_id, data)


@router.get("/list/", response_model=list[UserShowSchema], tags=["user"])
async def get_user_list(uow: uowDEP):
    return await UserService(uow).get_user_list()


@router.get("/get/{user_id}/", response_model=UserShowSchema, tags=["user"])
async def get_user_by_id(uow: uowDEP, user_id: int):
    return await UserService(uow).get_user_by_id(user_id)


@router.delete("/delete/{user_id}/", status_code=status.HTTP_204_NO_CONTENT, tags=["user"])
async def delete_user(uow: uowDEP, user_id: int):
    await UserService(uow).delete_user(user_id)


@router.post("/login/", response_model=JWTTokensData, tags=["user"])
async def login_user(uow: uowDEP, data: LoginUserSchema):
    return await UserService(uow).login_user(data)


@router.post("/token/access_from_refresh/", response_model=AccessTokenData, tags=["jwt token"])
async def refresh_token(uow: uowDEP, data: TokenVerifyOrRefreshSchema):
    return await UserService(uow).access_from_refresh(data)


@router.post("/token/is_valid/", response_model=bool, tags=["jwt token"])
async def verify_token(uow: uowDEP, data: TokenVerifyOrRefreshSchema, refresh: bool = False):
    return await UserService(uow).is_valid_token(data, refresh)
