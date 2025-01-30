import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class IdColMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, sort_order=-1)


class TimeStampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
        doc="Created at",
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Updated at",
    )


class BaseModelMixin(IdColMixin, TimeStampMixin):
    pass
