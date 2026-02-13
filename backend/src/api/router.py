from fastapi import APIRouter

from .v1.router import router as v1_router

api_router = APIRouter(prefix="/api")

# Подключаем все роутеры
api_router.include_router(v1_router)
