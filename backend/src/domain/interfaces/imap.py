from abc import ABC, abstractmethod

class IMAPClient(ABC):
	"""Порт - абстракция, не зависящая от внешнего мира"""

	@abstractmethod
	async def cloudflare_get_verify_link(self, email_address: str, password: str) -> str:
		pass
