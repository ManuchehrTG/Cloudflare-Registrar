import logging

from schemas.domain_ip_pair import DomainIPPair, DomainIPPairError, DomainIPPairResults

logger = logging.getLogger(__name__)

class DomainIPPairParser:
	"""Сервис для парсинга домен:IP пар"""

	def parse(self, text: str) -> DomainIPPairResults:
		"""
		Парсит текст в список DomainIPPair
		Возвращает результат с успешными парами и ошибками
		"""
		pairs = []
		errors = []
		lines = text.split("\n")

		for i, line in enumerate(lines, 1):
			line = line.strip()
			if not line:
				continue

			# Проверка наличия разделителя
			if ':' not in line:
				errors.append(DomainIPPairError(
					line_number=i,
					error="Нет разделителя ':'",
					raw_line=line
				))
				logger.error(f"Строка {i}: нет разделителя ':'")
				continue

			# Парсинг
			try:
				domain, ip = line.split(":", 1)
				domain = domain.strip()
				ip = ip.strip()
				
				# Валидация через модель
				pair = DomainIPPair(domain=domain, server_ip=ip)
				pairs.append(pair)

			except ValueError as e:
				errors.append(DomainIPPairError(
					line_number=i,
					error=str(e),
					raw_line=line
				))
				logger.error(f"Строка {i}: {str(e)}")
			except Exception as e:
				errors.append(DomainIPPairError(
					line_number=i,
					error=f"Неожиданная ошибка: {str(e)}",
					raw_line=line
				))

		return DomainIPPairResults(pairs=pairs, errors=errors)
