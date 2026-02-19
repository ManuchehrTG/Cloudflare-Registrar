# pyright: reportCallIssue=false

from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Literal

from .schemas import AppSettings, CelerySettings, LoggerSettings, RedisSettings, TelegramBotSettings, NamecheapSettings

class Settings(BaseSettings):
	environment: Literal["local", "staging", "production"]
	debug: bool

	domain: str = Field(validation_alias="TELEGRAM_BOT_DOMAIN")
	host: str = Field(validation_alias="TELEGRAM_BOT_HOST")
	port: int = Field(validation_alias="TELEGRAM_BOT_PORT")

	api_domain: str = Field(validation_alias="BACKEND_DOMAIN")

	app: AppSettings = AppSettings()
	celery: CelerySettings = CelerySettings()
	logger: LoggerSettings = LoggerSettings()
	redis: RedisSettings = RedisSettings()
	telegram_bot: TelegramBotSettings = TelegramBotSettings()

	namecheap: NamecheapSettings = NamecheapSettings()

	class Config:
		extra = "ignore"
		env_file = [".env"]
		env_file_encoding = "utf-8"

settings = Settings()
