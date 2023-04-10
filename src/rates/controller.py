from datetime import date
from typing import List, Literal, Optional

from aiohttp import ClientResponseError
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.nbrb_api.api import NBRBApi
from src.nbrb_api.api_types import RateDict
from src.rates.dal import RateDAL
from src.rates.schemas import RateCreate, RatePost, RateReturn


class RateController:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._dal = RateDAL(session)

    @classmethod
    def get_rate_schemas(cls, rate_list: List[RateDict]) -> List[RateCreate]:
        return [
            RateCreate(
                currency_id=rate["Cur_ID"],
                date=NBRBApi.get_rate_date(rate["Date"]),
                currency_abbreviation=rate["Cur_Abbreviation"],
                currency_scale=rate["Cur_Scale"],
                currency_name=rate["Cur_Name"],
                currency_rate=rate["Cur_OfficialRate"],
            )
            for rate in rate_list
        ]

    async def save_rates(self, rate: RatePost) -> Literal["Ok"]:
        if not rate:
            rate = RatePost()
        exchange_date = rate.date or date.today()
        try:
            rates = await NBRBApi.get_rates(exchange_date)
        except ClientResponseError as e:
            raise HTTPException(
                400, f"nbrb api answered with: {e.message}. Status code {e.status}"
            )
        schemas = self.get_rate_schemas(rates)
        try:
            async with self._session.begin():
                self._dal.bulk_create(schemas)
        except IntegrityError:
            raise HTTPException(400, "Rates from this date are already saved")
        return "Ok"

    async def get_rate(
        self, currency_code: int, exchange_date: Optional[date]
    ) -> RateReturn:
        rate, previous_rate = await self._dal.get_single_with_dynamic(
            currency_code, exchange_date or date.today()
        )
        if not rate:
            raise HTTPException(status_code=404, detail="Rate not found")
        dynamic = (
            rate.currency_rate - previous_rate if previous_rate is not None else None
        )
        rate_return = RateReturn(**rate.__dict__, dynamic=dynamic)
        return rate_return
