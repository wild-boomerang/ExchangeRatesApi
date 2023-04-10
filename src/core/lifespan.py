from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.db.init_db import init_db
from src.nbrb_api.api import NBRBApi


async def on_app_startup(_: FastAPI) -> None:
    await init_db()


async def on_app_shutdown(_: FastAPI) -> None:
    await NBRBApi.HTTP_SESSION.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_app_startup(app)
    yield
    await on_app_shutdown(app)
