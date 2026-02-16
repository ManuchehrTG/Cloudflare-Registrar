from abc import ABC, abstractmethod

class ProxyClient(ABC):
	"""Proxy - абстракция"""

	@abstractmethod
	def connection(self, proxy: str) -> None:
		pass

	@abstractmethod
	def get_ip(self) -> str | None:
		pass
