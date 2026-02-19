from typing import Any, Dict

class NamecheapError(Exception):
	"""Базовый класс для всех ошибок Namecheap SDK"""
	def __init__(self, message: str, code: int | None = None, raw_response: Dict[str, Any] | None = None, **kwargs):
		super().__init__(message)
		self.message = message
		self.code = code
		self.raw_response = raw_response
		self.details = {**kwargs}

class NamecheapAPIError(NamecheapError):
	"""Ошибка от API Namecheap (статус ERROR в ответе)"""
	pass
