from pydantic import BaseModel, Field

class CloudflareGetVerifyLinkRequest(BaseModel):
	email: str = Field(..., description="Email почты")
	password: str = Field(..., description="Пароль почты")
	proxy: str | None = Field(None, description="Прокси")

class CloudflareVerifyLinkResponse(BaseModel):
	email: str = Field(..., description="Верификационный email")
	link: str = Field(..., description="Верификационная ссылка от cloudflare")
	ip: str | None = Field(None, description="IP с которого выполнена задача")


class CloudflareAccountDataRequest(BaseModel):
	email: str = Field(..., description="Email")
	password: str = Field(..., description="Password")
	api_key: str = Field(..., description="API KEY")

class CloudflareAccountDataResponse(BaseModel):
	status: str = Field(..., description="Статус")
