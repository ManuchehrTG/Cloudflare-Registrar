import httpx
import xmltodict
from typing import Any, Dict, List

from .exceptions import NamecheapAPIError
from schemas.namecheap import NamecheapAccount

class NamecheapClient:
	"""Клиент для работы с Namecheap API"""
	def __init__(self, account: NamecheapAccount) -> None:
		self.base_url = "https://api.namecheap.com/xml.response"
		self._account = account
		self._client = httpx.AsyncClient(timeout=15)

	def _params(self, payload: Dict[str, Any]) -> Dict[str, Any]:
		params = self._account._to_api_params()
		params.update(payload)
		return params

	async def _request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
		request_params = self._params(params)

		try:
			response = await self._client.request(method, self.base_url, params=request_params)
			response.raise_for_status()

			data = xmltodict.parse(response.text)
			api_response = data.get("ApiResponse", {})

			if api_response.get("@Status") == "ERROR":
				self._handle_api_error(api_response)

			return api_response.get("CommandResponse", {})

		except httpx.HTTPError as e:
			raise

	def _handle_api_error(self, api_response: Dict[str, Any]):
		"""Обработка ошибок API - создает и кидает правильное исключение"""
		command = api_response.get("RequestedCommand")
		errors = api_response.get("Errors", {})
		error = errors.get("Error", {})

		message = error.get("#text", "Unknown error")
		code = error.get("@Number")

		raise NamecheapAPIError(
			message=message,
			code=code,
			raw_response=api_response,
			command=command,
		)

	async def get_domain(self, domain: str) -> Dict[str, Any]:
		params = {
			"Command": "namecheap.domains.getinfo",
			"DomainName": domain
		}
		return await self._request("GET", params=params)

	async def set_custom_domain_dns(self, domain: str, ns: List[str]) -> Dict[str, Any]:
		sld, tld = domain.split(".")
		ns_str = ",".join(ns)
		params = {
			"Command": "namecheap.domains.dns.setCustom",
			"SLD": sld,
			"TLD": tld,
			"NameServers": ns_str
		}
		return await self._request("POST", params=params)
