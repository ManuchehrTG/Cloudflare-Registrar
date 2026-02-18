from fastapi import Depends

from src.core.config import settings
from src.application.cloudflare.use_cases.get_verify_link import CloudflareGetVerifyLink
from src.application.cloudflare.use_cases.write_account_data import CloudflareWriteAccountData
from src.application.cloudflare.use_cases.generate_ns import CloudflareGenerateNS
from src.domain.interfaces.imap import IMAPClient
from src.domain.interfaces.proxy import ProxyClient
from src.domain.interfaces.text_storage import TextStorage
from src.domain.interfaces.cloudflare import CloudflareProvider
from src.infrastructure.services.imap.gmx_imap_client import GMXIMAPClient
from src.infrastructure.services.proxy.socks5 import ProxySocks5
from src.infrastructure.services.storage.text_storage import TextStorageService
from src.infrastructure.services.cloudflare.cloudflare import CloudflareService

def get_imap_client() -> IMAPClient:
	return GMXIMAPClient()

def get_proxy_client() -> ProxyClient:
	return ProxySocks5()

def get_text_storage_service() -> TextStorage:
	return TextStorageService(file_path=settings.storage.cf_accounts_file_path)

def get_cloudflare_service() -> CloudflareProvider:
	return CloudflareService()

def get_cloudflare_get_verify_link(
	proxy_client: ProxyClient = Depends(get_proxy_client),
	imap_client: IMAPClient = Depends(get_imap_client)
):
	return CloudflareGetVerifyLink(proxy_client, imap_client)

def get_cloudflare_write_account_data(
	text_storage_service: TextStorage = Depends(get_text_storage_service),
):
	return CloudflareWriteAccountData(text_storage_service)

def get_cloudflare_generate_ns(
	text_storage_service: TextStorage = Depends(get_text_storage_service),
	cloudflare_service: CloudflareProvider = Depends(get_cloudflare_service),
):
	return CloudflareGenerateNS(text_storage_service, cloudflare_service)
