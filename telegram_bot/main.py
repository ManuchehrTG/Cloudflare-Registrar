import asyncio
import uvicorn
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Update
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.container import container
from core.config import settings
from core.logger import setup_logging
from infrastructure.redis import redis
from middlewares import register_middlewares

async def create_app() -> FastAPI:
	storage = RedisStorage(redis)
	dp = Dispatcher(storage=storage)
	bot = Bot(token=settings.telegram_bot.token, default=DefaultBotProperties(parse_mode="HTML"))

	container.bot = bot

	register_middlewares(dp=dp)

	from handlers import router

	dp.include_router(router)

	logger.info("🟢 The bot is running!")

	@asynccontextmanager
	async def lifespan(app: FastAPI):
		try:
			await bot.set_webhook(url=f"{settings.domain}/webhook")
			yield  # Здесь работает приложение
		except Exception as e:
			logger.error(f"⚠️ Startup failed: {e}", exc_info=True)
			raise
		finally:
			logger.info("🔴 Shutting down...")
			try:
				await bot.delete_webhook()
				await bot.session.close()
				await dp.storage.close()
				await redis.aclose()
				logger.info("🤖 Aiogram bot session closed")
			except Exception as e:
				logger.error(f"Error during shutdown: {e}", exc_info=True)

	# Создание экземпляра FastAPI
	app = FastAPI(
		title=settings.app.title,
		version="1.0.0",
		lifespan=lifespan,
		docs_url="/api/docs" if settings.debug else None
	)

	# Настройка CORS
	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"]
	)

	@app.post("/webhook")
	async def bot_webook(update: dict):
		"""Обработка обновлений через вебхук."""
		try:
			telegram_update = Update(**update)
			await dp.feed_update(bot=bot, update=telegram_update)
		except Exception as e:
			logger.exception(f"Error processing update: {e}")
		finally:
			return {"status": "ok"}

	@app.get("/health-bot")
	async def health_check():
		return {"message": "ok", "status": "healthy"}

	return app

async def main() -> None:
	app = await create_app()

	config = uvicorn.Config(app=app, host=settings.host, port=settings.port, log_level="info", access_log=False)
	server = uvicorn.Server(config)

	await server.serve()

if __name__ == "__main__":
	setup_logging()
	logger = logging.getLogger()

	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		logger.info("🔴 Server stopped gracefully")
