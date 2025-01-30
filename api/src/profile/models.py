from typing import Optional

from enum import Enum as PyEnum

from slugify import slugify

from sqlalchemy import event
from sqlalchemy.orm import Mapped, Mapper, mapped_column
from sqlalchemy.dialects.postgresql import ENUM

from ..core.db.base import Base
from ..core.db.mixins import BaseModelMixin

from .enums import ProfileLinkTypeEnum


class Profile(BaseModelMixin, Base):
    username: Mapped[str] = mapped_column(nullable=False, index=True)
    template_username: Mapped[str] = mapped_column(nullable=False, index=True)
    steam_id: Mapped[Optional[str]] = mapped_column(nullable=True, index=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    avatar_frame_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    location: Mapped[Optional[str]] = mapped_column(nullable=True)
    location_flag_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    player_level: Mapped[Optional[int]] = mapped_column(nullable=True)
    link_type: Mapped[PyEnum] = mapped_column(
        ENUM(
            ProfileLinkTypeEnum,
            name="profile_link_type",
            create_type=True,
        ),
        nullable=False,
        default=ProfileLinkTypeEnum.with_username,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(nullable=False, index=True, default=True)
    slug: Mapped[str] = mapped_column(nullable=False, index=True, unique=True)

    def __str__(self) -> str:
        return f"Profile - {self.username}"


def generate_slug(mapper: Mapper, connection, target: Profile) -> None:
    target.slug = slugify(
        target.steam_id
        if target.steam_id and target.link_type == ProfileLinkTypeEnum.with_steam_id
        else target.username
    )


event.listen(Profile, "before_insert", generate_slug)
event.listen(Profile, "before_update", generate_slug)
