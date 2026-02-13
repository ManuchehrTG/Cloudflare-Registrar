from fastapi import APIRouter

from .imap.endpoints import router as imap_router

router = APIRouter(prefix="/v1")

# Подключаем все роутеры
router.include_router(imap_router)
