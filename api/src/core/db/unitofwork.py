from abc import ABC
from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import create_async_session_maker

from ...repositories.profile import ProfileRepository


class AbstractUnitOfWork(ABC):
    profile: ProfileRepository

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError()

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def flush(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()

    @abstractmethod
    async def add(self, instance):
        raise NotImplementedError()

    @abstractmethod
    async def add_all(self, instances):
        raise NotImplementedError()


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self._session_factory = create_async_session_maker()

    async def __aenter__(self):
        self._session: AsyncSession = self._session_factory()

        # Initialize repositories
        self.profile = ProfileRepository(self._session)

        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self._session.close()

    async def commit(self):
        await self._session.commit()

    async def flush(self):
        await self._session.flush()

    async def rollback(self):
        await self._session.rollback()

    async def add(self, instance):
        self._session.add(instance)

    async def add_all(self, instances):
        self._session.add_all(instances)
