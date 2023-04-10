from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.crc32 import CRC32Route
from src.core.dependencies import get_db_session
from src.rates.controller import RateController
from src.rates.schemas import RatePost, RateReturn

rate_router = APIRouter(route_class=CRC32Route)


@rate_router.post("/")
async def save_exchange_rates(
    rate: RatePost = None,
    session: AsyncSession = Depends(get_db_session),
) -> Literal["Ok"]:
    controller = RateController(session)
    return await controller.save_rates(rate)


@rate_router.get("/{currency_code}", response_model=RateReturn)
async def get_exchange_rate(
    currency_code: int,
    exchange_date: date = None,
    session: AsyncSession = Depends(get_db_session),
) -> RateReturn:
    controller = RateController(session)
    return await controller.get_rate(currency_code, exchange_date)
