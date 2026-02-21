from contextlib import asynccontextmanager
from fastapi import FastAPI
from .core.config import settings
from .core.db import init_db
from .api.main import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (cleanup code would go here if needed)


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_V1_STR)