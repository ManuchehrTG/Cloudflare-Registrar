from pydantic import BaseModel
from typing import Any, Dict

class CloudflareNSResult(BaseModel):
	"""Результат обработки одного домена"""
	success: bool
	domain: str
	ip: str
	data: Dict[str, Any] | None = None
	error: str | None = None
	status_code: int | None = None
