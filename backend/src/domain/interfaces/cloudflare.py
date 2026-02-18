from abc import ABC, abstractmethod
from typing import List

class CloudflareProvider(ABC):
	"""Cloudflare - абстракция"""

	@abstractmethod
	async def generate_ns(self, api_key: str, domain: str, ip: str) -> List[str]:
		pass
