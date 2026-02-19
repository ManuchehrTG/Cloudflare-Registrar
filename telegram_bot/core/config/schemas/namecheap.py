from pydantic_settings import BaseSettings

class NamecheapSettings(BaseSettings):
	api_key: str
	api_username: str
	nc_username: str
	client_ip: str

	class Config:
		env_prefix = "NAMECHEAP_"
		case_sensitive = False
