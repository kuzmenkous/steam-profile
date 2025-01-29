from typing import Annotated, Optional

from fastapi import Depends, Query

from .config import settings


class PaginationParams:
    def __init__(
        self,
        page: Optional[int] = Query(ge=1, default=None),
        size: int = Query(ge=1, le=500, default=settings.pagination.limit_per_page),
    ):
        self.page = page
        self.size = size

    @property
    def params_dict(self):
        return {"page": self.page, "limit": self.size}


pagination_params = Annotated[PaginationParams, Depends()]
