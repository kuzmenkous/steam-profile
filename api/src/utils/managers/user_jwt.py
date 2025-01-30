import datetime
import logging

from jose import jwt
from jose import JWTError

from ...core.config import settings

from .dto import JWTTokensResponse, JWTTokenData


log = logging.getLogger(__name__)

TOKEN_TYPE = "Bearer"


class JWTTokensManager:
    @staticmethod
    async def generate_token(
        user_id: int,
        refresh: bool = False,
    ) -> str:
        expire = settings.jwt.refresh_token_expire if refresh else settings.jwt.access_token_expire
        expire_timedelta = datetime.timedelta(minutes=expire)
        expire_time = datetime.datetime.now(datetime.UTC) + expire_timedelta

        claims = {
            "exp": expire_time,
            "sub": str(user_id),
            "refresh": refresh,
        }

        encoded_jwt = jwt.encode(
            claims=claims,
            key=settings.app.secret_key,
            algorithm=settings.jwt.algorithm,
        )
        return encoded_jwt

    async def generate_access_token(
        self,
        user_id: int,
    ) -> str:
        return await self.generate_token(
            user_id,
        )

    async def generate_refresh_token(
        self,
        user_id: int,
    ) -> str:
        return await self.generate_token(
            user_id,
            refresh=True,
        )

    async def generate_tokens_for_user(
        self,
        user_id: int,
    ) -> JWTTokensResponse:
        return JWTTokensResponse(
            access_token=await self.generate_access_token(user_id),
            refresh_token=await self.generate_refresh_token(user_id),
            token_type="bearer",
        )

    async def get_decoded_token(self, jwt_token: str) -> dict | None:
        return jwt.decode(
            jwt_token.replace(TOKEN_TYPE, "").strip()
            if jwt_token.startswith(TOKEN_TYPE)
            else jwt_token,
            settings.app.secret_key,
            algorithms=[settings.jwt.algorithm],
        )

    async def is_token_valid_bearer(self, jwt_token: str) -> bool:
        if jwt_token.startswith(TOKEN_TYPE) or jwt_token.startswith(TOKEN_TYPE):
            return True
        return False

    async def check_token_exp_valid(self, decoded_token: dict) -> bool:
        try:
            exp = decoded_token["exp"]
            current_time = datetime.datetime.now(datetime.UTC)
            if current_time < datetime.datetime.fromtimestamp(exp, datetime.UTC):
                return True
            else:
                return False
        except JWTError:
            return False
        except (Exception,):
            return False

    async def is_token_valid(
        self,
        jwt_token: str,
        decoded_token: str,
        refresh: bool = False,
    ) -> bool:
        try:
            token_valid_bearer = await self.is_token_valid_bearer(jwt_token)
            token_exp_valid = await self.check_token_exp_valid(decoded_token)
            if any([not token_valid_bearer, not token_exp_valid]):
                return False
            if refresh and not decoded_token.get("refresh"):
                return False
            return True
        except JWTError:
            return False
        except (Exception,):
            return False

    async def get_jwt_token_data(
        self,
        jwt_token: str,
        refresh: bool = False,
    ) -> JWTTokenData | None:
        try:
            decoded_token = await self.get_decoded_token(jwt_token)
            if not await self.is_token_valid(jwt_token, decoded_token, refresh):
                return None
            return JWTTokenData(
                user_id=decoded_token["sub"],
                refresh=decoded_token.get("refresh"),
            )
        except (JWTError, KeyError) as e:
            log.exception(e)
            return None
