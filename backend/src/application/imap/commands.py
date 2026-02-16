from pydantic import BaseModel

class CloudflareGetVerifyLinkCommand(BaseModel):
	email: str
	password: str
	proxy: str | None
