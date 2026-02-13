from .base import BaseAppError

class InfrastructureError(BaseAppError):
	"""Исключения инфраструктурного слоя (5xx)"""
	layer = "infrastructure"
	error_code = "infrastructure_error"


class DatabaseError(InfrastructureError):
	"""Ошибки базы данных"""
	error_code = "database_error"

class ExternalServiceError(InfrastructureError):
	"""Ошибки внешних сервисов"""
	error_code = "external_service_error"

	def __init__(self, service: str, message: str | None = None, **kwargs):
		if not message:
			message = f"Service '{service}' is unavailable"
		details = {"service": service, **kwargs.pop("details", {})}

		super().__init__(message, details=details, **kwargs)
