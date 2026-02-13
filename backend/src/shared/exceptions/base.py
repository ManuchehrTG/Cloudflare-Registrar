from typing import Dict, Any

class BaseAppError(Exception):
	"""Корневое исключение всего приложения"""

	# Дефолтные значения
	default_message: str = "An error occurred"
	error_code: str = "internal_error"
	layer: str = "unknown"

	def __init__(
		self,
		message: str | None = None,
		code: str | None = None,
		details: Dict[str, Any] | None = None,
		original_error: Exception | None = None,
		**kwargs
	):
		self.message = message or self.default_message
		self.code = code or self.error_code
		self.details = details or {}
		self.details.update(kwargs)
		self.original_error = original_error
		self.layer = getattr(self, 'layer', 'unknown')

		super().__init__(self.message)

	def __str__(self) -> str:
		if self.details:
			return f"{self.message} | {self.details}"
		return self.message

	def to_dict(self) -> dict:
		"""Сериализация для API-ответов"""
		result = {
			"error": self.code,
			"message": self.message,
			"details": self.details,
			"layer": self.layer
		}
		if self.original_error:
			result["original_error"] = str(self.original_error)
		return result
