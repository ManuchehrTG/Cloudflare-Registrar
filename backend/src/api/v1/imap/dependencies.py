from fastapi import Depends

from src.application.imap.interfaces import IMAPClient
from src.infrastructure.imap.gmx_imap_client import GMXIMAPClient
from src.application.imap.use_cases.cloudflare_get_verify_link import CloudflareGetVerifyLink

def get_imap_client() -> IMAPClient:
	return GMXIMAPClient()

def get_cloudflare_get_verify_link(
	imap_client: IMAPClient = Depends(get_imap_client)
):
	return CloudflareGetVerifyLink(imap_client)
