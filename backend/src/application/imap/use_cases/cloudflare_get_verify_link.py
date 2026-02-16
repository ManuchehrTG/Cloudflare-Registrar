from src.application.decorators import handle_domain_errors
from src.application.imap.commands import CloudflareGetVerifyLinkCommand
from src.application.imap.dtos import CloudflareVerifyLinkDTO
from src.application.imap.interfaces import IMAPClient

class CloudflareGetVerifyLink:
	def __init__(self, imap_client: IMAPClient):
		self._imap_client = imap_client

	@handle_domain_errors
	async def execute(self, command: CloudflareGetVerifyLinkCommand):
		link = await self._imap_client.cloudflare_get_verify_link(email_address=command.email, password=command.password, proxy=command.proxy)
		return CloudflareVerifyLinkDTO(email=command.email, link=link)
