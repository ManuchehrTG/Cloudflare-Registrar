import logging

from src.application.decorators import handle_domain_errors
from src.application.cloudflare.commands import CloudflareGenerateNSCommand
from src.application.cloudflare.dtos import CloudflareNSDTO
from src.domain.interfaces.text_storage import TextStorage
from src.domain.interfaces.cloudflare import CloudflareProvider

logger = logging.getLogger()

class CloudflareGenerateNS:
	def __init__(self, text_storage_service: TextStorage, cloudflare_service: CloudflareProvider):
		self._text_storage_service = text_storage_service
		self.cloudflare_service = cloudflare_service

	@handle_domain_errors
	async def execute(self, command: CloudflareGenerateNSCommand):
		line = await self._text_storage_service.pop_first() # email:password:api_key
		domain, ip = command.domain, command.ip

		if not line:
			logger.warning("Line is empty. Line: %s", line)
			return

		try:
			email, password, api_key = line.split(":")
		except Exception as e:
			logger.exception("The string is not cloudflare account data. Line: %s", line)
			return

		try:
			ns_list = await self.cloudflare_service.generate_ns(api_key, domain, ip)
			return CloudflareNSDTO(email=email, password=password, ns=ns_list)
		except Exception as e:
			logger.error("Generate ns error: %s", str(e))
