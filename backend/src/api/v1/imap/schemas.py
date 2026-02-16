from pydantic import BaseModel, Field

class CloudflareGetVerifyLinkRequest(BaseModel):
	email: str = Field(..., description="Email почты")
	password: str = Field(..., description="Пароль почты")
	proxy: str = Field(..., description="Прокси")

class CloudflareVerifyLinkResponse(BaseModel):
	email: str = Field(..., description="Верификационный email")
	link: str = Field(..., description="Верификационная ссылка от cloudflare")
	ip: str | None = Field(None, description="IP с которого выполнена задача")

	class Config:
		from_attributes = True
