from fastapi import APIRouter

from .cloudflare.endpoints import router as cloudflare_router

router = APIRouter(prefix="/v1")

# Подключаем все роутеры
router.include_router(cloudflare_router)
