from fastapi import HTTPException
from functools import wraps
from typing import Callable, TypeVar

from src.shared.exceptions import BaseAppError, InfrastructureError, NotFoundError, BusinessRuleError, UnprocessableEntityError

T = TypeVar('T')

def handle_domain_errors(func: Callable[..., T]) -> Callable[..., T]:
	"""Декоратор для автоматического маппинга доменных ошибок"""
	@wraps(func)
	async def wrapper(*args, **kwargs) -> T:
		# print(f"DEBUG: func={func.__name__}, args={args}, kwargs={kwargs}")
		try:
			return await func(*args, **kwargs) # pyright: ignore

		except InfrastructureError as e:
			raise HTTPException(status_code=503, detail=e.to_dict())

		except NotFoundError as e:
			raise HTTPException(status_code=404, detail=e.to_dict())
		except UnprocessableEntityError as e:
			raise HTTPException(status_code=422, detail=e.to_dict())
		except BusinessRuleError as e:
			raise HTTPException(status_code=409, detail=e.to_dict())
		except BaseAppError as e:
			# Общие доменные ошибки -> 400
			raise HTTPException(status_code=400, detail=e.to_dict())
	return wrapper # pyright: ignore
