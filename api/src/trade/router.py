from fastapi import APIRouter, status

from ..core.db.dependencies import uowDEP

from .schemas import TradeUpdateSchema, TradeShowSchema
from .service import TradeService


router = APIRouter(
    prefix="/trade",
    tags=["Trade"],
)


@router.get("/get/", response_model=TradeShowSchema, status_code=status.HTTP_200_OK)
async def get_trade(uow: uowDEP):
    return await TradeService(uow).get_or_create_trade()


@router.put("/update/", response_model=TradeShowSchema, status_code=status.HTTP_200_OK)
async def update_trade(data: TradeUpdateSchema, uow: uowDEP):
    return await TradeService(uow).update_trade(data)
