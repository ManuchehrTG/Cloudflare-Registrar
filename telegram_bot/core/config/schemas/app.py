from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List

class AppSettings(BaseSettings):
	title: str
	languages: List[str] = Field(default_factory=list)
	default_language: str
	time_zone: str

	class Config:
		env_prefix = "APP_"
		case_sensitive = False
