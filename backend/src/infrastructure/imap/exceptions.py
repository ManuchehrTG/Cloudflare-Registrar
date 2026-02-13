from src.shared.exceptions.infrastructure import InfrastructureError, ExternalServiceError

# class IMAPConnectionError(ExternalServiceError):
#     """Ошибка подключения к IMAP серверу"""
#     error_code = "imap_connection_error"

#     def __init__(self, host: str, port: int = None, **kwargs):
#         message = f"Cannot connect to IMAP server {host}"
#         if port:
#             message += f":{port}"
#         super().__init__(
#             service="GMX IMAP",
#             message=message,
#             details={"host": host, "port": port},
#             **kwargs
#         )

class IMAPAuthenticationError(ExternalServiceError):
	"""Ошибка аутентификации IMAP"""
	error_code = "imap_authentication_error"

	def __init__(self, email: str, **kwargs):
		message = f"Authentication failed for {email}"
		details = {"email": email}
		super().__init__(service="GMX IMAP", message=message, details=details, **kwargs)

class EmailNotFoundError(InfrastructureError):
	"""Письмо не найдено"""
	error_code = "email_not_found_error"

	def __init__(self, email: str, search_criteria: dict | None = None, **kwargs):
		message = f"No matching emails found for {email}"
		details = {"email": email}
		if search_criteria:
			details["search_criteria"] = search_criteria				# pyright: ignore[reportArgumentType]
		super().__init__(message, details=details, **kwargs)

class MessageNotFoundError(InfrastructureError):
	"""Сообщение не найдено"""
	error_code = "message_not_found_error"

	def __init__(self, email: str, **kwargs):
		message = f"Message data not found in email for {email}"
		details = {"email": email}
		super().__init__(message, details=details, **kwargs)

class VerificationLinkNotFoundError(InfrastructureError):
	"""Ссылка верификации не найдена в письме"""
	error_code = "verification_link_not_found"

	def __init__(self, email: str, **kwargs):
		message = f"Verification link not found in email for {email}"
		details = {"email": email}
		super().__init__(message, details=details, **kwargs)
