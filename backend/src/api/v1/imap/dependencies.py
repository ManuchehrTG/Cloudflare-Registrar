from fastapi import Depends

from src.application.imap.interfaces import IMAPClient
from src.application.imap.use_cases.cloudflare_get_verify_link import CloudflareGetVerifyLink
from src.domain.interfaces.proxy_client import ProxyClient
from src.infrastructure.imap.gmx_imap_client import GMXIMAPClient
from src.infrastructure.proxy.socks5 import ProxySocks5

def get_imap_client() -> IMAPClient:
	return GMXIMAPClient()

def get_proxy_client() -> ProxyClient:
	return ProxySocks5()

def get_cloudflare_get_verify_link(
	proxy_client: ProxyClient = Depends(get_proxy_client),
	imap_client: IMAPClient = Depends(get_imap_client)
):
	return CloudflareGetVerifyLink(proxy_client, imap_client)
