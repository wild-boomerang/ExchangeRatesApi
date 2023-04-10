from fastapi import FastAPI

from src.core.config import settings
from src.core.lifespan import lifespan
from src.core.routers import root_router

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
app.include_router(root_router)
