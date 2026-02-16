import logging
import socks
import socket

from src.domain.interfaces.proxy_client import ProxyClient

logger = logging.getLogger()

class ProxySocks5(ProxyClient):
	def connection(self, proxy: str) -> None:
		try:
			parts = proxy.split(':')
			host = parts[0]
			port = int(parts[1])
			username = parts[2]
			password = parts[3]

			socks.set_default_proxy(
				socks.SOCKS5,
				host,
				port,
				username=username,
				password=password
			)

			socket.socket = socks.socksocket
		except Exception as e:
			logger.warning("Failed use proxy:", str(e))

	def get_ip(self) -> str | None:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("8.8.8.8", 80))  # Google DNS
			local_ip = s.getsockname()[0]
			s.close()
			return local_ip
		except Exception as e:
			logger.warning("Failed get ip:", str(e))
