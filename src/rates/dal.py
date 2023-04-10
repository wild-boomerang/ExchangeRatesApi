import decimal
from datetime import date, timedelta
from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.rates.models import Rate
from src.rates.schemas import RateCreate


class RateDAL:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def bulk_create(self, rate_schemas: List[RateCreate]) -> None:
        rate_models = [Rate(**rate.dict()) for rate in rate_schemas]
        self._session.add_all(rate_models)

    async def get_single(self, currency_id: int, rate_date: date) -> Optional[Rate]:
        return await self._session.scalar(
            select(Rate).where(Rate.currency_id == currency_id, Rate.date == rate_date)
        )

    async def get_single_with_dynamic(
        self, currency_id: int, rate_date: date
    ) -> Tuple[Optional[Rate], Optional[decimal.Decimal]]:
        current_rate = await self.get_single(currency_id, rate_date)
        previous_rate = None
        if current_rate:
            previous_rate = await self._session.scalar(
                select(Rate.currency_rate).where(
                    Rate.currency_id == currency_id,
                    Rate.date == rate_date - timedelta(1),
                )
            )
        return current_rate, previous_rate
