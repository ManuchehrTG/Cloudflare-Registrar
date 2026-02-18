import logging
import httpx
from typing import List

# from .exceptions import EmailNotFoundError, IMAPAuthenticationError, MessageNotFoundError, VerificationLinkNotFoundError
from src.infrastructure.services.cloudflare.exceptions import CloudflareServiceError, CloudflareAccountsNotFoundError, NSIsNotListError
from src.domain.interfaces.cloudflare import CloudflareProvider

logger = logging.getLogger()

class CloudflareService(CloudflareProvider):
	"""Адаптер - конкретная реализация для GMX"""
	def __init__(self) -> None:
		self.base_url = "https://api.cloudflare.com/client/v4"
		self._http_client = httpx.AsyncClient(proxy="http://plan-limited-country-any:96nsvm0kgcg0qhx0@relay-eu.proxyshard.com:8080")

	async def generate_ns(self, api_key: str, domain: str, ip: str) -> List[str]:
		try:
			test_response = await self._http_client.get(
				"http://api.ipify.org",  # Простой HTTP сайт (не HTTPS для теста)
				timeout=10.0
			)
			proxy_ip = test_response.text
			logger.info(f"Прокси IP (через ipify): {proxy_ip}")

			cf_test = await self._http_client.get(
				"https://api.cloudflare.com/client/v4/accounts",
				headers={"Authorization": f"Bearer {api_key}"}
			)
			logger.info(f"Статус от Cloudflare: {cf_test.status_code}")
		except Exception as e:
			logger.error(f"Прокси не работает: {e}")

		try:

			account_id = await self._get_account_id(api_key)
			zone = await self._get_or_create_zone(api_key, account_id, domain)

			await self._disable_robots_txt_management(api_key, zone["id"])

			await self._clear_dns(api_key, zone["id"])
			await self._create_dns_record(api_key, zone["id"], "A", domain, ip)
			await self._create_dns_record(api_key, zone["id"], "A", f"www.{domain}", ip)

			ns = await self._get_ns(api_key, zone["id"])

		except (CloudflareServiceError, CloudflareAccountsNotFoundError, NSIsNotListError):
			raise
		except Exception as e:
			raise CloudflareServiceError(message="Error [generate_ns]", original_errors=str(e))

		if not isinstance(ns, list):
			raise NSIsNotListError(ns=ns)

		return ns

	async def _get_account_id(self, api_key: str) -> str:
		# print(">>> _get_account_id")
		# print("base_url:", self.base_url)
		# print("api_key:", api_key)
		response = await self._http_client.get(f"{self.base_url}/accounts", headers={"Authorization": f"Bearer {api_key}"})
		response.raise_for_status()

		data = response.json()

		if not data.get("success"):
			raise CloudflareServiceError(message=f"API Error [_get_account_id]: {data.get('errors', 'Unknown error')}")

		accounts = data.get("result", [])
		if not accounts:
			raise CloudflareAccountsNotFoundError()

		return accounts[0]["id"]

	async def _get_or_create_zone(self, api_key: str, account_id: str, domain: str):
		zone = await self._get_zone_by_domain(api_key, domain)
		if not zone:
			zone = await self._create_zone(api_key, account_id, domain)

		return zone

	async def _get_zone_by_domain(self, api_key: str, domain: str):
		"""Получает зону по домену, если существует"""
		response = await self._http_client.get(
			f"{self.base_url}/zones",
			headers={"Authorization": f"Bearer {api_key}"},
			params={"name": domain}
		)
		response.raise_for_status()
		zones = response.json()["result"]
		return zones[0] if zones else None

	async def _create_zone(self, api_key: str, account_id: str, domain: str):
		response = await self._http_client.post(
			f"{self.base_url}/zones",
			headers={"Authorization": f"Bearer {api_key}"},
			json={
				"name": domain,
				"account": {"id": account_id},
				"jump_start": False
			}
		)
		response.raise_for_status()

		data = response.json()
		if not data["success"]:
			raise CloudflareServiceError(message="Create zone error", details=data)

		return data["result"]

	async def _disable_robots_txt_management(self, api_key: str, zone_id: str):
		"""Отключает автоматическое управление robots.txt"""

		# Сначала получаем текущую конфигурацию
		get_response = await self._http_client.get(
			f"{self.base_url}/zones/{zone_id}/bot_management",
			headers={"Authorization": f"Bearer {api_key}"}
		)
		current_config = get_response.json()["result"]

		# Обновляем только нужный параметр
		update_payload = {
			**current_config,  # сохраняем все текущие настройки
			"is_robots_txt_managed": False
		}

		# Удаляем поля, которые могут быть проблемными
		if "stale_zone_configuration" in update_payload:
			del update_payload["stale_zone_configuration"]

		response = await self._http_client.put(
			f"{self.base_url}/zones/{zone_id}/bot_management",
			headers={"Authorization": f"Bearer {api_key}"},
			json=update_payload
		)

		data = response.json()
		if not data["success"]:
			raise CloudflareServiceError(message=f"API Error [_disable_robots_txt_management]: {data.get('errors')}")

		return data["result"]

	async def _clear_dns(self, api_key: str, zone_id: str) -> int:
		"""
		Удаляет ВСЕ DNS записи зоны, которые разрешено удалять через API.
		Возвращает количество удалённых записей.
		"""

		deleted_count = 0
		page = 1
		per_page = 100

		while True:
			response = await self._http_client.get(
				f"{self.base_url}/zones/{zone_id}/dns_records",
				headers={"Authorization": f"Bearer {api_key}"},
				params={
					"page": page,
					"per_page": per_page
				}
			)
			response.raise_for_status()

			data = response.json()
			if not data.get("success"):
				raise CloudflareServiceError(message="api/zones/{id}/get_dns_records Error", details=data.get("errors"))

			records = data["result"]
			if not records:
				break

			for record in records:
				record_id = record["id"]

				try:
					delete_resp = await self._http_client.delete(
						f"{self.base_url}/zones/{zone_id}/dns_records/{record_id}",
						headers={"Authorization": f"Bearer {api_key}"}
					)
					delete_resp.raise_for_status()
					deleted_count += 1

				except httpx.HTTPStatusError as e:
					logger.warning(f"Cloudflare не даст удалить системные записи (NS, SOA): {e}")
					pass

			if len(records) < per_page:
				break

			page += 1

		return deleted_count


	async def _create_dns_record(self, api_key: str, zone_id: str, record_type: str, name: str, content: str, proxied=True):
		url = f"{self.base_url}/zones/{zone_id}/dns_records"
		payload = {
			"type": record_type,
			"name": name,
			"content": content,
			"ttl": 1,
			"proxied": proxied
		}

		response = await self._http_client.post(url, headers={"Authorization": f"Bearer {api_key}"}, json=payload)
		response.raise_for_status()
		return response.json()

	async def _get_ns(self, api_key: str, zone_id: str):
		url = f"{self.base_url}/zones/{zone_id}"
		response = await self._http_client.get(url, headers={"Authorization": f"Bearer {api_key}"})
		response.raise_for_status()

		return response.json()["result"]["name_servers"]
