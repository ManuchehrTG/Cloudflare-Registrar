from abc import ABC, abstractmethod
from typing import List

class TextStorage(ABC):
	"""TextStorage - абстракция"""

	@abstractmethod
	async def append(self, record: str) -> None:
		pass

	@abstractmethod
	async def pop_first_n(self, count: int) -> List[str]:
		pass

	@abstractmethod
	async def pop_first(self) -> str | None:
		pass
