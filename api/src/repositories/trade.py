from pydantic import BaseModel

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..trade.models import Trade

from .generic import Repository


class TradeRepository(Repository[Trade]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Trade)

    async def update_trade(self, data: BaseModel):
        stmt = (
            update(self.model).values(data.model_dump(exclude_unset=True)).returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_trade(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        return res.scalars().first()
