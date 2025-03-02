from typing import Optional

from pydantic import BaseModel

from ..core.schemas.base import MainSchema


class TradeCreateSchema(BaseModel):
    partner: str
    token: str


class TradeUpdateSchema(BaseModel):
    partner: Optional[str] = None
    token: Optional[str] = None


class TradeShowSchema(MainSchema):
    partner: str
    token: str
