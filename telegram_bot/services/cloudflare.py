import asyncio
import httpx
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging
# from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

@dataclass
class CloudflareResult:
	"""Результат обработки одного домена"""
	success: bool
	domain: str
	data: Optional[Dict[str, Any]] = None
	error: Optional[str] = None
	status_code: Optional[int] = None

class CloudflareService:
	"""Сервис для работы с Cloudflare API"""

	def __init__(self, api_domain: str, timeout: int = 60, max_retries: int = 3):
		self.api_domain = api_domain
		self.timeout = timeout
		self.max_retries = max_retries
		self._client: Optional[httpx.AsyncClient] = None

	async def __aenter__(self):
		"""Контекстный менеджер для автоматического закрытия клиента"""
		self._client = httpx.AsyncClient(
			timeout=self.timeout,
			limits=httpx.Limits(max_keepalive_connections=10, max_connections=20)
		)
		return self

	async def __aexit__(self, *args):
		if self._client:
			await self._client.aclose()

	# @retry(
	# 	stop=stop_after_attempt(3),
	# 	wait=wait_exponential(multiplier=1, min=2, max=10),
	# 	retry=retry_if_exception_type((
	# 		httpx.TimeoutException,
	# 		httpx.NetworkError,
	# 		httpx.HTTPStatusError
	# 	)),
	# 	before_sleep=lambda retry_state: logger.warning(
	# 		f"Retry {retry_state.attempt_number} for Cloudflare API"
	# 	)
	# )
	async def _make_request(self, domain: str, ip: str) -> Dict[str, Any]:
		"""
		Внутренний метод с повторными попытками
		"""
		url = f"https://{self.api_domain}/api/v1/cloudflare/generate_ns"

		response = await self._client.post(
			url,
			json={"domain": domain, "ip": ip},
			headers={"User-Agent": "TelegramBot/1.0"}
		)

		# Проверяем статус
		response.raise_for_status()

		# Парсим JSON
		data = response.json()

		# Проверяем структуру ответа
		if not isinstance(data, list):
			raise ValueError(f"Unexpected response format: {data}")

		return data

	async def process_batch(self, pairs: List['DomainIPPair']) -> List[CloudflareResult]:
		"""
		Обрабатывает пачку доменов
		"""
		results = []

		for pair in pairs:
			try:
				logger.info(f"Processing {pair.domain} -> {pair.server_ip}")

				# Делаем запрос с ретраями
				data = await self._make_request(pair.domain, pair.server_ip)

				# Проверяем что получили
				if data and isinstance(data, list) and len(data) > 0:
					results.append(CloudflareResult(
						success=True,
						domain=pair.domain,
						data=data[0]  # Берем первый элемент
					))
				else:
					results.append(CloudflareResult(
						success=False,
						domain=pair.domain,
						error="Empty response from API"
					))
					
			except httpx.TimeoutException:
				logger.error(f"Timeout for {pair.domain}")
				results.append(CloudflareResult(
					success=False,
					domain=pair.domain,
					error="Timeout after 3 retries",
					status_code=408
				))
				
			except httpx.HTTPStatusError as e:
				logger.error(f"HTTP error for {pair.domain}: {e.response.status_code}")
				results.append(CloudflareResult(
					success=False,
					domain=pair.domain,
					error=f"API error: {e.response.status_code}",
					status_code=e.response.status_code
				))

			except Exception as e:
				logger.error(f"Unexpected error for {pair.domain}: {str(e)}")
				results.append(CloudflareResult(
					success=False,
					domain=pair.domain,
					error=f"Unexpected error: {str(e)[:100]}"
				))

			# Небольшая задержка между запросами
			await asyncio.sleep(0.5)

		return results
