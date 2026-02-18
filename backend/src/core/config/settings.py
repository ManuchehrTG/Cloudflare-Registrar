# pyright: reportCallIssue=false

from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Literal

from .schemas import AppSettings, StorageSettings

class Settings(BaseSettings):
	environment: Literal["local", "staging", "production"]

	debug: bool
	allowed_origins: List[str] = Field(default_factory=list)
	allowed_hosts: List[str] = Field(default_factory=list)

	domain: str = Field(validation_alias="BACKEND_DOMAIN")
	host: str = Field(validation_alias="BACKEND_HOST")
	port: int = Field(validation_alias="BACKEND_PORT")

	app: AppSettings = AppSettings()
	storage: StorageSettings = StorageSettings()

	class Config:
		env_file = [".env"]
		env_file_encoding = "utf-8"

settings = Settings()
