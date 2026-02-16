from pydantic import BaseModel

class CloudflareVerifyLinkDTO(BaseModel):
	email: str
	link: str
	ip: str | None
