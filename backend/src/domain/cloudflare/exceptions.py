from src.shared.exceptions.domain import DomainError

class EmptyAccountDataError(DomainError):
	"""Пустые данные аккаунта"""
	def __init__(self):
		super().__init__(
			message="No Cloudflare account data available",
		)
