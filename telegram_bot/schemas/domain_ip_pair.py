import re
from pydantic import BaseModel, field_validator
from typing import List

class DomainIPPair(BaseModel):
	domain: str
	server_ip: str

	@field_validator("domain")
	@classmethod
	def validate_domain(cls, v):
		# Простая валидация домена
		domain_pattern = r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
		if not re.match(domain_pattern, v):
			raise ValueError(f"Некорректный домен: {v}")
		return v.lower()

	@field_validator("server_ip")
	@classmethod
	def validate_ip(cls, v):
		# Валидация IPv4
		ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
		if not re.match(ip_pattern, v):
			raise ValueError(f"Некорректный IP: {v}")

		# Проверка, что числа в диапазоне 0-255
		parts = v.split(".")
		for part in parts:
			if int(part) > 255:
				raise ValueError(f"IP должен быть в диапазоне 0-255: {v}")
		return v

class DomainIPPairError(BaseModel):
	line_number: int
	error: str
	raw_line: str

class DomainIPPairResults(BaseModel):
	pairs: List[DomainIPPair]
	errors: List[DomainIPPairError]
