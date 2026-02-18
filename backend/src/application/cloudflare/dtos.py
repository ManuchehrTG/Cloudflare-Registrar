from pydantic import BaseModel
from typing import List

class CloudflareVerifyLinkDTO(BaseModel):
	email: str
	link: str
	ip: str | None

class CloudflareNSDTO(BaseModel):
	email: str
	password: str
	ns: List[str]
