import asyncio
import aiofiles
import os
from pathlib import Path
from typing import List

from src.domain.interfaces.text_storage import TextStorage

class TextStorageService(TextStorage):
	def __init__(self, file_path: str):
		self.file_path = Path(file_path)
		self.file_path.parent.mkdir(parents=True, exist_ok=True)
		self.file_path.touch(exist_ok=True)
		self._lock = asyncio.Lock()

	# Внутренние методы
	async def _read_lines(self) -> List[str]:
		async with aiofiles.open(self.file_path, "r", encoding="utf-8") as f:
			lines = await f.readlines()

			# Фильтруем пустые строки в конце
			while lines and not lines[-1].strip():
				lines.pop()

			return lines

	async def _atomic_write(self, lines: List[str]) -> None:
		temp_path = self.file_path.with_suffix(".tmp")

		async with aiofiles.open(temp_path, "w", encoding="utf-8") as f:
			await f.writelines(lines)

		os.replace(temp_path, self.file_path)  # атомарная замена

	# 1. Добавить запись
	async def append(self, record: str) -> None:
		async with self._lock:
			async with aiofiles.open(self.file_path, "a", encoding="utf-8") as f:
				await f.write(record.rstrip("\n") + "\n")

	# 2. Получить первые N и удалить
	async def pop_first_n(self, count: int) -> List[str]:
		async with self._lock:
			lines = await self._read_lines()

			if not lines:
				return []

			selected = lines[:count]
			remaining = lines[count:]

			await self._atomic_write(remaining)

			return [line.strip() for line in selected]

	# 3. Получить первую и удалить
	async def pop_first(self) -> str | None:
		async with self._lock:
			lines = await self._read_lines()

			if not lines:
				return None

			first = lines[0]
			remaining = lines[1:]

			await self._atomic_write(remaining)

			return first.strip()
