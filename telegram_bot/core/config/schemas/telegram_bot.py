from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List

class TelegramBotSettings(BaseSettings):
	token: str
	admin_ids: List[int] = Field(default_factory=list)

	class Config:
		env_prefix = "TELEGRAM_BOT_"
		case_sensitive = False
