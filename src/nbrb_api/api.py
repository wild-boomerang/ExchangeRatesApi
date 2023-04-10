from datetime import date, datetime
from typing import List

import aiohttp

from src.nbrb_api.api_types import RateDict


class NBRBApi:
    BASE_URL = "https://www.nbrb.by"
    BEL_RUBLE_EXCHANGE_RATE = "/api/exrates/rates"
    BEL_RUBLE_DYNAMIC_RATE = "/api/exrates/rates/dynamics"

    HTTP_SESSION: aiohttp.ClientSession

    @classmethod
    def init_http_session(cls) -> None:
        cls.HTTP_SESSION = aiohttp.ClientSession(cls.BASE_URL)

    @classmethod
    async def close_http_session(cls) -> None:
        await cls.HTTP_SESSION.close()

    @classmethod
    def get_rate_date(cls, api_date: str) -> date:
        return datetime.fromisoformat(api_date).date()

    @classmethod
    async def get_rates(cls, exchange_date: date) -> List[RateDict]:
        iso_date = exchange_date.isoformat()
        params = {"ondate": iso_date, "periodicity": 0}
        async with cls.HTTP_SESSION.get(
            cls.BEL_RUBLE_EXCHANGE_RATE, params=params
        ) as response:
            rates: List[RateDict] = await response.json()
        return rates
