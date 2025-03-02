from ..core.db.base import Base
from ..core.db.mixins import BaseModelMixin

from sqlalchemy.orm import Mapped, mapped_column


class Trade(BaseModelMixin, Base):
    partner: Mapped[str] = mapped_column(nullable=False, index=True)
    token: Mapped[str] = mapped_column(nullable=False, index=True)

    def __str__(self):
        return f"Trade - {self.partner}"
