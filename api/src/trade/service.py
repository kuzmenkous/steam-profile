import logging

from sqlalchemy.exc import SQLAlchemyError

from ..core.db.service import BaseService

from .schemas import TradeCreateSchema, TradeUpdateSchema, TradeShowSchema


log = logging.getLogger(__name__)


class TradeService(BaseService):
    async def get_or_create_trade(self) -> TradeShowSchema:
        try:
            async with self.uow:
                trade = await self.uow.trade.get_trade()
                if not trade:
                    trade = await self.uow.trade.create_instance(
                        obj_in=TradeCreateSchema(
                            partner="1970605216",
                            token="hK3VWGgL",
                        )
                    )
                    await self.uow.add(trade)
                    await self.uow.commit()
                return TradeShowSchema.model_validate(trade)
        except SQLAlchemyError as e:
            log.exception(e)

    async def update_trade(self, data: TradeUpdateSchema) -> TradeShowSchema:
        try:
            async with self.uow:
                trade = await self.uow.trade.update_trade(data)
                await self.uow.commit()
                trade = await self.uow.trade.get_trade()
                return TradeShowSchema.model_validate(trade)
        except SQLAlchemyError as e:
            log.exception(e)
