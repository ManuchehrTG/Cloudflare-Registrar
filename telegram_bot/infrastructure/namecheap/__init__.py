from .client import NamecheapClient
from core.config import settings
from schemas.namecheap import NamecheapAccount

account = NamecheapAccount(
	api_key=settings.namecheap.api_key,
	api_username=settings.namecheap.api_username,
	nc_username=settings.namecheap.nc_username,
	client_ip=settings.namecheap.client_ip,
)

namecheap_client = NamecheapClient(account)

__all__ = ["namecheap_client"]
