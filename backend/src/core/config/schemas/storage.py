from pydantic_settings import BaseSettings

class StorageSettings(BaseSettings):
	dir: str = "storage"

	@property
	def cf_accounts_file_path(self) -> str:
		return f"{self.dir}/cloudflare/accounts.txt"

	class Config:
		env_prefix = "STORAGE_"
		case_sensitive = False
