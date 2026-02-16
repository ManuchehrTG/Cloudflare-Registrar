import aioimaplib
import email
import re
from email.message import Message

from src.application.imap.interfaces import IMAPClient
from src.infrastructure.imap.exceptions import EmailNotFoundError, IMAPAuthenticationError, MessageNotFoundError, VerificationLinkNotFoundError
from src.shared.exceptions.infrastructure import ExternalServiceError

class GMXIMAPClient(IMAPClient):
	"""Адаптер - конкретная реализация для GMX"""

	async def cloudflare_get_verify_link(self, email_address: str, password: str) -> str:
		mail = None
		try:
			# Здесь конкретная реализация с imaplib
			mail = aioimaplib.IMAP4_SSL(host="imap.gmx.com", timeout=30)
			await mail.wait_hello_from_server()

			try:
				await mail.login(email_address, password)
				await mail.select("INBOX")
			except Exception as e:
				raise IMAPAuthenticationError(email_address, original_error=str(e))

			# Ищем письма от Cloudflare
			_, messages = await mail.search('FROM "cloudflare.com"')
			email_ids = messages[0].split()

			if not email_ids:
				raise EmailNotFoundError(email_address, search_criteria={"from": "cloudflare.com"})

			# Берем последнее письмо
			latest_id = email_ids[-1].decode("utf-8")
			result, msg_data = await mail.fetch(latest_id, "(RFC822)")

			if result == 'OK' and msg_data:
				for response in msg_data:
					if isinstance(response, bytearray):
						# msg_bytes = line[1] if len(line) > 1 else line[0]
						msg = email.message_from_bytes(response)
						break

			else:
				raise MessageNotFoundError(email_address)

			# Достаем текст

			body = self._extract_text_from_email(msg)

			# Ищем ссылку верификации
			match = re.search(r'(https://dash\.cloudflare\.com/email-verification\?token=[^\s]+)', body)

			if not match:
				raise VerificationLinkNotFoundError(email_address)

			return match.group(1)

		except aioimaplib.Abort as e:
			raise ExternalServiceError(service="Imap", original_error=str(e))
		finally:
			if mail:
				try:
					await mail.close()
					await mail.logout()
				except:
					pass

	def _extract_text_from_email(self, msg: Message) -> str:
		"""Извлекает текст из email безопасно"""
		try:
			if msg.is_multipart():
				for part in msg.walk():
					content_type = part.get_content_type()
					if content_type == "text/plain":
						payload = part.get_payload(decode=True)
						if payload:
							return payload.decode('utf-8', errors='replace')
			else:
				payload = msg.get_payload(decode=True)
				if payload:
					return payload.decode('utf-8', errors='replace')
			
			# Fallback на сырой текст
			return str(msg.get_payload()) or ""
			
		except Exception:
			return ""
