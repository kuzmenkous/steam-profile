from typing import Optional

from pydantic import BaseModel

from ..core.schemas.base import MainSchema

from .enums import ProfileLinkTypeEnum


class CreateProfileSchema(BaseModel):
    template_username: str
    steam_id: Optional[str] = None
    link_type: ProfileLinkTypeEnum
    steam_link: str


class CreateProfileDataToDBSchema(BaseModel):
    template_username: str
    username: str
    steam_id: Optional[str] = None
    avatar_url: Optional[str] = None
    avatar_frame_url: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    location_flag_url: Optional[str] = None
    player_level: Optional[int] = None
    link_type: ProfileLinkTypeEnum
    steam_link: str


class UpdateProfileSchema(BaseModel):
    template_username: Optional[str] = None
    username: Optional[str] = None
    steam_id: Optional[str] = None
    avatar_url: Optional[str] = None
    avatar_frame_url: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    location_flag_url: Optional[str] = None
    player_level: Optional[int] = None
    link_type: Optional[ProfileLinkTypeEnum] = None
    is_active: Optional[bool] = None
    is_steam_authenticated: Optional[bool] = None


class ProfileShowResponseSchema(MainSchema):
    id: int
    template_username: str
    username: str
    steam_id: Optional[str] = None
    avatar_url: Optional[str] = None
    avatar_frame_url: str
    description: str
    location: str
    location_flag_url: str
    player_level: int
    link_type: ProfileLinkTypeEnum
    steam_link: Optional[str] = None
    is_active: bool
    is_steam_authenticated: Optional[bool] = None
    slug: str
    invite_link_path: Optional[str] = None
