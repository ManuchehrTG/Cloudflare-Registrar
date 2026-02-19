from pydantic import BaseModel, Field
from typing import Any, Dict, List

class NamecheapAccount(BaseModel):
	api_username: str = Field(..., description="Username required to access the API")
	api_key: str = Field(..., description="Password required used to access the API")
	nc_username: str = Field(..., description="The Username on which a command is executed.Generally, the values of ApiUser and UserName parameters are the same.")
	client_ip: str = Field(..., description="An IP address of the server from which our system receives API calls (only IPv4 can be used).")

	def _to_api_params(self) -> Dict[str, Any]:
		"""Конвертация в параметры для API Namecheap"""
		return {
			"ApiUser": self.api_username,
			"ApiKey": self.api_key,
			"UserName": self.nc_username,
			"ClientIp": self.client_ip,
		}

class NamecheapDomain(BaseModel):
	domain: str
	is_owner: bool
	host_count: int
	ns: List[str] = Field(default_factory=list)

class OperationResult(BaseModel):
	success: bool
	message: str | None = None
	error_code: int | None = None
