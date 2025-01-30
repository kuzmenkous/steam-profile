from dataclasses import dataclass, asdict

from typing import Optional


@dataclass
class ProfileCreateDataDTO:
    username: str
    avatar_url: str
    steam_id: Optional[str] = None
    avatar_frame_url: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    location_flag_url: Optional[str] = None
    player_level: Optional[int] = None

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class JWTTokensResponse:
    access_token: str
    refresh_token: str
    token_type: str

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class JWTTokenData:
    user_id: str
    refresh: bool = False
