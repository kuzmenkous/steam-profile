import logging

from sqlalchemy.exc import SQLAlchemyError

from ..core.db.service import BaseService

from ..utils.managers.steam_parse import SteamParseManager

from .schemas import (
    CreateProfileSchema,
    CreateProfileDataToDBSchema,
    UpdateProfileSchema,
    ProfileShowResponseSchema,
)


log = logging.getLogger(__name__)


class ProfileService(BaseService):
    async def create_profile(self, data: CreateProfileSchema) -> ProfileShowResponseSchema:
        try:
            async with self.uow:
                if await self.uow.profile.exists_profile_by_template_username(
                    template_username=data.template_username,
                ):
                    raise ValueError("Profile with this username already exists")
                if data.steam_id and await self.uow.profile.exists_profile_by_steam_id(
                    steam_id=data.steam_id
                ):
                    raise ValueError("Profile with this Steam ID already exists")
                profile_parse_data = await SteamParseManager().create_page(
                    data.steam_link, data.template_username
                )
                create_data = CreateProfileDataToDBSchema(
                    **profile_parse_data.dict(),
                    template_username=data.template_username,
                    link_type=data.link_type,
                    steam_id=data.steam_id,
                    steam_link=data.steam_link,
                )
                profile = await self.uow.profile.create_instance(obj_in=create_data)
                await self.uow.add(profile)
                await self.uow.commit()
                return ProfileShowResponseSchema.model_validate(profile)
        except SQLAlchemyError as e:
            log.exception(e)

    async def update_profile(
        self,
        profile_id: int,
        data: UpdateProfileSchema,
    ) -> ProfileShowResponseSchema:
        try:
            async with self.uow:
                profile = await self.uow.profile.get_profile_by_id(
                    profile_id=profile_id,
                )
                template_username = profile.template_username
                if not profile:
                    raise ValueError("Profile not found")
                update_data = data.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(profile, field, value)
                await self.uow.add(profile)
                await self.uow.commit()
                await SteamParseManager().edit_page(
                    template_username=template_username,
                    new_template_username=profile.template_username
                    if profile.template_username != template_username
                    else None,
                    username=profile.username,
                    avatar_url=profile.avatar_url,
                    avatar_frame_url=profile.avatar_frame_url,
                    description=profile.description,
                    location=profile.location,
                    location_flag_url=profile.location_flag_url,
                    player_level=profile.player_level,
                )
                return ProfileShowResponseSchema.model_validate(profile)
        except SQLAlchemyError as e:
            log.exception(e)

    async def get_profiles(self):
        try:
            async with self.uow:
                profiles = await self.uow.profile.get_list()
                return [ProfileShowResponseSchema.model_validate(profile) for profile in profiles]
        except SQLAlchemyError as e:
            log.exception(e)

    async def get_profile(self, slug: str) -> str:
        try:
            async with self.uow:
                profile = await self.uow.profile.get_profile_by_slug(slug=slug)
                if not profile:
                    raise ValueError("Profile not found")
                return await SteamParseManager().get_page(profile.template_username)
        except SQLAlchemyError as e:
            log.exception(e)

    async def get_profile_by_id(self, profile_id: int) -> ProfileShowResponseSchema:
        try:
            async with self.uow:
                profile = await self.uow.profile.get_profile_by_id(profile_id=profile_id)
                if not profile:
                    raise ValueError("Profile not found")
                return ProfileShowResponseSchema.model_validate(profile)
        except SQLAlchemyError as e:
            log.exception

    async def delete_profile(self, profile_id: int):
        try:
            async with self.uow:
                profile = await self.uow.profile.get_profile_by_id(profile_id=profile_id)
                await self.uow.profile.delete(obj_id=profile_id)
                await self.uow.commit()
                await SteamParseManager().delete_page(profile.template_username)
        except SQLAlchemyError as e:
            log.exception(e)
