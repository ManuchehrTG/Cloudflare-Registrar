from pydantic import BaseModel, Field

class CloudflareGetVerifyLinkRequest(BaseModel):
	email: str = Field(..., description="Email почты")
	password: str = Field(..., description="Пароль почты")

class CloudflareVerifyLinkResponse(BaseModel):
	email: str = Field(..., description="Верификационный email")
	link: str = Field(..., description="Верификационная ссылка от cloudflare")

	class Config:
		from_attributes = True
