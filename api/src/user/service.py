import logging

from sqlalchemy.exc import SQLAlchemyError

from ..core.db.service import BaseService

from ..utils.managers.user_jwt import JWTTokensManager

from .schemas import (
    UserCreateSchema,
    UserUpdateSchema,
    UserShowSchema,
    LoginUserSchema,
    JWTTokensData,
    AccessTokenData,
    TokenVerifyOrRefreshSchema,
)


log = logging.getLogger(__name__)


class UserService(BaseService):
    async def create_user(self, data: UserCreateSchema) -> UserShowSchema:
        try:
            async with self.uow:
                if await self.uow.user.user_exists_by_email(data.email):
                    raise ValueError("User with this email already exists")
                user = await self.uow.user.create_instance(obj_in=data)
                await self.uow.add(user)
                await self.uow.commit()
                return UserShowSchema(id=user.id, email=user.email, is_active=user.is_active)
        except SQLAlchemyError as e:
            log.error(e)

    async def update_user(self, user_id: int, data: UserUpdateSchema) -> UserShowSchema:
        try:
            async with self.uow:
                user = await self.uow.user.get_user_by_id(user_id)
                if not user:
                    raise ValueError("User not found")
                user = await self.uow.user.update_instance(obj=user, obj_in=data)
                await self.uow.add(user)
                await self.uow.commit()
                return UserShowSchema(id=user.id, email=user.email, is_active=user.is_active)
        except SQLAlchemyError as e:
            log.error(e)

    async def get_user_by_id(self, user_id: int) -> UserShowSchema:
        try:
            async with self.uow:
                user = await self.uow.user.get_user_by_id(user_id)
                if not user:
                    raise ValueError("User not found")
                return UserShowSchema(id=user.id, email=user.email, is_active=user.is_active)
        except SQLAlchemyError as e:
            log.error(e)

    async def get_user_list(self) -> list[UserShowSchema]:
        try:
            async with self.uow:
                users = await self.uow.user.get_list()
                return [
                    UserShowSchema(id=user.id, email=user.email, is_active=user.is_active)
                    for user in users
                ]
        except SQLAlchemyError as e:
            log.error(e)

    async def delete_user(self, user_id: int) -> None:
        try:
            async with self.uow:
                user = await self.uow.user.get_user_by_id(user_id)
                if not user:
                    raise ValueError("User not found")
                await self.uow.delete(user)
                await self.uow.commit()
        except SQLAlchemyError as e:
            log.error(e)

    async def login_user(self, data: LoginUserSchema) -> JWTTokensData:
        try:
            async with self.uow:
                user = await self.uow.user.get_user_by_email(data.email)
                if not user:
                    raise ValueError("User not found")
                if not user.check_password(data.password):
                    raise ValueError("Incorrect password")
                tokens_data = await JWTTokensManager().generate_tokens_for_user(user_id=user.id)
                return JWTTokensData(**tokens_data.dict())
        except SQLAlchemyError as e:
            log.exception(e)

    async def is_valid_token(self, data: TokenVerifyOrRefreshSchema, refresh: bool = False) -> bool:
        try:
            async with self.uow:
                token_data = await JWTTokensManager().get_jwt_token_data(data.token, refresh)
                if not token_data:
                    return False
                user = await self.uow.user.get_user_by_id(int(token_data.user_id))
                if not user:
                    return False
                return True
        except SQLAlchemyError as e:
            log.exception(e)
            return False

    async def access_from_refresh(self, data: TokenVerifyOrRefreshSchema) -> AccessTokenData:
        try:
            async with self.uow:
                token_data = await JWTTokensManager().get_jwt_token_data(data.token)
                if not token_data:
                    raise ValueError("Invalid token")
                user = await self.uow.user.get_user_by_id(int(token_data.user_id))
                if not user:
                    raise ValueError("User not found")
                token = await JWTTokensManager().generate_access_token(user_id=user.id)
                return AccessTokenData(access_token=token)
        except SQLAlchemyError as e:
            log.exception(e)
            return False
