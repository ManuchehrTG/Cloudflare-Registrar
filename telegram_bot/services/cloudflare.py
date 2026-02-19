import asyncio
import httpx
import logging
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from schemas.cloudflare import CloudflareNSResult
from schemas.domain_ip_pair import DomainIPPair

logger = logging.getLogger(__name__)

class CloudflareService:
	"""Сервис для работы с Cloudflare API"""

	def __init__(self, api_domain: str, timeout: int = 60, max_retries: int = 3):
		self.api_domain = api_domain
		self.timeout = timeout
		self.max_retries = max_retries
		self._client = httpx.AsyncClient(timeout=self.timeout)

	@retry(
		stop=stop_after_attempt(3),
		wait=wait_exponential(multiplier=1, min=2, max=10),
		retry=retry_if_exception_type((
			httpx.TimeoutException,
			httpx.NetworkError,
			httpx.HTTPStatusError
		)),
		before_sleep=lambda retry_state: logger.warning(
			f"Retry {retry_state.attempt_number} for Cloudflare API"
		)
	)
	async def _make_request(self, domain: str, ip: str) -> Dict[str, Any]:
		"""
		Внутренний метод с повторными попытками
		"""
		url = f"https://{self.api_domain}/api/v1/cloudflare/generate_ns"

		response = await self._client.post(url, json={"domain": domain, "ip": ip})

		# Проверяем статус
		response.raise_for_status()

		# Парсим JSON
		data = response.json()

		# Проверяем структуру ответа
		if not isinstance(data, dict):
			raise ValueError(f"Unexpected response format: {data}")

		return data

	async def process_batch(self, pairs: List[DomainIPPair]) -> List[CloudflareNSResult]:
		"""
		Обрабатывает пачку доменов
		"""
		results: List[CloudflareNSResult] = []

		for pair in pairs:
			try:
				logger.info(f"Processing {pair.domain} -> {pair.server_ip}")

				# Делаем запрос с ретраями
				data = await self._make_request(pair.domain, pair.server_ip)

				# Проверяем что получили
				if data.get("email") and data.get("password") and data.get("ns"):
					results.append(CloudflareNSResult(
						success=True,
						domain=pair.domain,
						ip=pair.server_ip,
						data=data
					))
				else:
					results.append(CloudflareNSResult(
						success=False,
						domain=pair.domain,
						ip=pair.server_ip,
						data=data,
						error="Empty response from API",
					))

			except httpx.TimeoutException:
				logger.error(f"Timeout for {pair.domain}")
				results.append(CloudflareNSResult(
					success=False,
					domain=pair.domain,
					ip=pair.server_ip,
					error="Timeout after 3 retries",
					status_code=408
				))

			except httpx.HTTPStatusError as e:
				logger.error(f"HTTP error for {pair.domain}: {e.response.status_code}")

				if e.response.status_code == 503:
					data = e.response.json()
					error = f"API error: {data['message']}"
				else:
					error = f"API error: {e.response.status_code}"

				results.append(CloudflareNSResult(
					success=False,
					domain=pair.domain,
					ip=pair.server_ip,
					error=error,
					status_code=e.response.status_code
				))

			except Exception as e:
				logger.error(f"Unexpected error for {pair.domain}: {str(e)}")
				results.append(CloudflareNSResult(
					success=False,
					domain=pair.domain,
					ip=pair.server_ip,
					error=f"Unexpected error: {str(e)[:100]}"
				))

			# Небольшая задержка между запросами
			await asyncio.sleep(0.5)

		return results
