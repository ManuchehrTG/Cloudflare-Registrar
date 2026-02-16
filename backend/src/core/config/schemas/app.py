from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List

class AppSettings(BaseSettings):
	debug: bool
	title: str
	allowed_origins: List[str] = Field(default_factory=list)
	allowed_hosts: List[str] = Field(default_factory=list)

	languages: List[str] = Field(default_factory=list)
	default_language: str
	storage_dir: str
	storage_cf_accounts: str

	domain: str
	host: str
	port: int

	class Config:
		env_prefix = "APP_"
		case_sensitive = False
