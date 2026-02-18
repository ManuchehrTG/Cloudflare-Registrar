from pydantic import BaseModel

class CloudflareGetVerifyLinkCommand(BaseModel):
	email: str
	password: str
	proxy: str | None

class CloudflareWriteAccountDataCommand(BaseModel):
	email: str
	password: str
	api_key: str

class CloudflareGenerateNSCommand(BaseModel):
	domain: str
	ip: str
