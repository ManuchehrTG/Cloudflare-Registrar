from uuid import UUID

from .base import BaseAppError

class DomainError(BaseAppError):
	"""Исключения доменного слоя (4xx бизнес-ошибки)"""
	layer = "domain"
	error_code = "domain_error"

class NotFoundError(DomainError):
	"""Сущность не найдена (можно использовать в любом слое)"""
	error_code = "not_found" # 404

	def __init__(self, entity: str, entity_id: str | UUID, search_type: str = "id", **kwargs):
		message = f"{entity} with {search_type} '{entity_id}' not found"
		details = {"entity": entity, "entity_id": entity_id}
		super().__init__(message, details=details, **kwargs)


class BusinessRuleError(DomainError):
	"""Конфликт - нарушение бизнес-правил"""
	error_code = "conflict_error" # 409


class UnprocessableEntityError(DomainError):
	"""Логическая ошибка"""
	error_code = "unprocessable_entity_error" # 422


class AccessDeniedError(DomainError):
	"""Отказ в доступе"""
	error_code = "access_denied" # 403
