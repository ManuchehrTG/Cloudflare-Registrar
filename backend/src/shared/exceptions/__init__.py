from .base import BaseAppError
from .domain import DomainError, NotFoundError, BusinessRuleError, AccessDeniedError, UnprocessableEntityError
# from .application import ApplicationError
from .infrastructure import InfrastructureError, DatabaseError, ExternalServiceError
# from .api import ApiError, UnauthorizedError, ForbiddenError, NotFoundApiError

"""
Корневые исключения приложения.
Иерархия:
BaseAppError
├── DomainError (бизнес-логика)
├── ApplicationError (use cases, сервисы)
├── InfrastructureError (БД, внешние API)
└── ApiError (HTTP-уровень)
"""
