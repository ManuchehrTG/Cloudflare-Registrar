# pyright: reportCallIssue=false

from pydantic_settings import BaseSettings
from typing import Literal

from .schemas import AppSettings

class Settings(BaseSettings):
	environment: Literal["local", "staging", "production"]

	app: AppSettings = AppSettings()

	class Config:
		env_file = [".env"]
		env_file_encoding = "utf-8"

settings = Settings()
