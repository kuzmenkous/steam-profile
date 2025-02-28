from sqlalchemy.ext.asyncio import AsyncSession

from ..profile.models import Profile

from .generic import Repository


class ProfileRepository(Repository[Profile]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Profile)

    async def get_profile_by_id(self, *, profile_id: int) -> Profile:
        return await self.get_one_by_id(obj_id=profile_id)

    async def get_profile_by_username(self, *, username: str) -> Profile:
        return await self.get_one_by_attr(attr=self.model.username, value=username)

    async def get_profile_by_steam_id(self, *, steam_id: str) -> Profile:
        return await self.get_one_by_attr(attr=self.model.steam_id, value=steam_id)

    async def get_profile_by_slug(self, *, slug: str) -> Profile:
        return await self.get_one_by_attr(attr=self.model.slug, value=slug)

    async def get_profile_by_invite_link_path(self, *, invite_link_path: str) -> Profile:
        return await self.get_one_by_attr(attr=self.model.invite_link_path, value=invite_link_path)

    async def exists_profile_by_id(self, *, profile_id: int) -> bool:
        return await self.exists_by_id(obj_id=profile_id)

    async def exists_profile_by_username(self, *, username: str) -> bool:
        return await self.exists_by_attr(attr=self.model.username, value=username)

    async def exists_profile_by_template_username(self, *, template_username: str) -> bool:
        return await self.exists_by_attr(attr=self.model.template_username, value=template_username)

    async def exists_profile_by_steam_id(self, *, steam_id: str) -> bool:
        return await self.exists_by_attr(attr=self.model.steam_id, value=steam_id)

    async def exists_by_invite_link_path(self, *, invite_link_path: str) -> bool:
        return await self.exists_by_attr(attr=self.model.invite_link_path, value=invite_link_path)
