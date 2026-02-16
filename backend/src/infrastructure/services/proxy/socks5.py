import logging
import socks
import socket
import urllib.request

from src.domain.interfaces.proxy import ProxyClient

logger = logging.getLogger()

class ProxySocks5(ProxyClient):
	def connection(self, proxy: str) -> None:
		try:
			host, port, username, password = proxy.split(':')

			socks.set_default_proxy(
				socks.SOCKS5,
				host,
				int(port),
				username=username,
				password=password
			)

			socket.socket = socks.socksocket
		except Exception as e:
			logger.exception("Failed use proxy")

	def get_ip(self) -> str | None:
		try:
			return urllib.request.urlopen("https://api.ipify.org").read().decode()
		except Exception as e:
			logger.warning("Failed get ip")
