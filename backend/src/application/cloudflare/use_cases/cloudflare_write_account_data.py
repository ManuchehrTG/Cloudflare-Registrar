from src.application.decorators import handle_domain_errors
from src.application.cloudflare.commands import CloudflareWriteAccountDataCommand
from src.domain.interfaces.text_storage import TextStorage

class CloudflareWriteAccountData:
	def __init__(self, text_storage_service: TextStorage):
		self._text_storage_service = text_storage_service

	@handle_domain_errors
	async def execute(self, command: CloudflareWriteAccountDataCommand):
		line = f"{command.email}:{command.password}:{command.api_key}"
		await self._text_storage_service.append(record=line)
