import logging
import socks
import socket
import urllib.request

from src.domain.interfaces.proxy import ProxyClient

logger = logging.getLogger()

class ProxySocks5(ProxyClient):
	def connection(self, proxy: str) -> None:
		try:
			print("connection...")
			host, port, username, password = proxy.split(':')

			print(f"{host}:{port}:{username}:{password}")

			socks.set_default_proxy(
				socks.SOCKS5,
				host,
				1080, # int(port),
				rdns=True,
				username=username,
				password=password
			)
			print("use socket...")
			socket.socket = socks.socksocket
			print("connection success")
		except Exception as e:
			logger.exception("Failed use proxy")

	def get_ip(self) -> str | None:
		try:
			print("get ip...")
			return urllib.request.urlopen("https://api.ipify.org", timeout=5).read().decode()
		except Exception as e:
			logger.warning("Failed get ip")
