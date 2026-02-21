from fastapi import APIRouter
from .routes import utils, items

api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(items.router)