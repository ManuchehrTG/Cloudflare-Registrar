from abc import ABC, abstractmethod

class IMAPClient(ABC):
	"""Порт - абстракция, не зависящая от внешнего мира"""

	@abstractmethod
	async def cloudflare_get_verify_link(self, email_address: str, password: str, proxy: str) -> str:
		pass

	# @abstractmethod
	# async def mark_as_read(self, email_address: str, message_id: str) -> None:
	# 	pass
