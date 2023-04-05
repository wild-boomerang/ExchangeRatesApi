import zlib
from contextlib import asynccontextmanager
from datetime import date, timedelta
from typing import Awaitable, Callable, Dict, List, Optional

import aiohttp
from fastapi import FastAPI, Request, Response
from fastapi.routing import APIRoute

BASE_URL = "https://www.nbrb.by"
BEL_RUBLE_EXCHANGE_RATE = "/api/exrates/rates"
BEL_RUBLE_DYNAMIC_RATE = "/api/exrates/rates/dynamics"

HTTP_SESSION: aiohttp.ClientSession

DB: Dict[str, List] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global HTTP_SESSION
    HTTP_SESSION = aiohttp.ClientSession(BASE_URL)
    yield
    await HTTP_SESSION.close()


class CRC32Route(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Awaitable[Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)

            crc32 = zlib.crc32(response.body)
            response.headers["X-Body-CRC32"] = str(crc32)
            return response

        return custom_route_handler


app = FastAPI(lifespan=lifespan)
app.router.route_class = CRC32Route


@app.get("/save_exchange_rates/{exchange_date}")
async def save_exchange_rates(exchange_date: Optional[date] = date.today()):
    iso_date = exchange_date.isoformat()
    params = {"ondate": iso_date, "periodicity": 0}
    async with HTTP_SESSION.get(BEL_RUBLE_EXCHANGE_RATE, params=params) as response:
        json_res = await response.json()
    DB[iso_date] = json_res
    return "Ok"


@app.get("/get_exchange_rate")
async def get_exchange_rate(
    currency_code: int, exchange_date: Optional[date] = date.today()
):
    url = f"{BEL_RUBLE_DYNAMIC_RATE}/{currency_code}"
    params = {
        "startdate": (exchange_date - timedelta(1)).isoformat(),
        "enddate": exchange_date.isoformat(),
    }
    async with HTTP_SESSION.get(url, params=params) as response:
        json_res = await response.json()
    return {"exchange_rates": json_res}
