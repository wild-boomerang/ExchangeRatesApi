from fastapi import APIRouter

from src.rates.router import rate_router

root_router = APIRouter()
root_router.include_router(rate_router, prefix="/rates", tags=["rates"])
