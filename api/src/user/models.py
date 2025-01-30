from sqlalchemy import event
from sqlalchemy.orm import mapped_column, Mapped, Mapper

from ..core.db.base import Base
from ..core.db.mixins import BaseModelMixin

from ..utils.hashing import Hashing


class User(BaseModelMixin, Base):
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    def check_password(self, password: str) -> bool:
        return Hashing.verify_password(password, self.password)

    def __str__(self):
        return f"Email: {self.email}. Active - {self.is_active}"


def hash_user_password(mapper: Mapper, connection, target: User) -> None:
    target.password = Hashing.get_hashed_password(target.password)


event.listen(User, "before_insert", hash_user_password)
event.listen(User, "before_update", hash_user_password)
