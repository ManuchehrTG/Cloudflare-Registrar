from src.application.decorators import handle_domain_errors
from src.application.cloudflare.commands import CloudflareGetVerifyLinkCommand
from src.application.cloudflare.dtos import CloudflareVerifyLinkDTO
from src.domain.interfaces.imap import IMAPClient
from src.domain.interfaces.proxy import ProxyClient

class CloudflareGetVerifyLink:
	def __init__(self, proxy_client: ProxyClient, imap_client: IMAPClient):
		self._proxy_client = proxy_client
		self._imap_client = imap_client

	@handle_domain_errors
	async def execute(self, command: CloudflareGetVerifyLinkCommand):
		if command.proxy:
			self._proxy_client.connection(command.proxy)

		ip = self._proxy_client.get_ip()

		link = await self._imap_client.cloudflare_get_verify_link(email_address=command.email, password=command.password)
		return CloudflareVerifyLinkDTO(email=command.email, link=link, ip=ip)
