import logging
from typing import List

from infrastructure.namecheap.client import NamecheapClient
from infrastructure.namecheap.exceptions import NamecheapError
from schemas.namecheap import OperationResult

logger = logging.getLogger(__name__)

class NamecheapService:
	def __init__(self, namecheap_client: NamecheapClient) -> None:
		self.namecheap_client = namecheap_client

	async def update_domain_ns(self, domain: str, ns: List[str]):
		try:
			result = await self.namecheap_client.set_custom_domain_dns(domain, ns)
			updated = result.get("DomainDNSSetCustomResult", {}).get("@Updated", "false") == "true"
			return OperationResult(success=updated)
		except NamecheapError as e:
			return OperationResult(success=False, message=e.message, error_code=e.code)
		except Exception as e:
			return OperationResult(success=False, message=str(e))
