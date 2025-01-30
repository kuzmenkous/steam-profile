from typing import Optional, TypeVar, Generic

from pydantic import BaseModel


Model = TypeVar("Model", bound=BaseModel)


class MainSchema(BaseModel):
    class Config:
        from_attributes = True


class PaginatedListSchema(MainSchema, Generic[Model]):
    objects_count: Optional[int] = None
    next_page: Optional[int] = None
    previous_page: Optional[int] = None
    pages_count: Optional[int] = None
    results: Optional[list[Model]] = None
