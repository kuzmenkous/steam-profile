from sqlalchemy.ext.asyncio import AsyncSession

from ..user.models import User

from .generic import Repository


class UserRepository(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.get_one_by_id(obj_id=user_id)

    async def get_user_by_email(self, email: str) -> User:
        return await self.get_one_by_attr(attr=self.model.email, value=email)

    async def user_exists_by_email(self, email: str) -> bool:
        return await self.exists_by_attr(attr=self.model.email, value=email)
