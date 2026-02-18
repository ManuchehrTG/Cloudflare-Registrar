from src.shared.exceptions.infrastructure import InfrastructureError, ExternalServiceError

class CloudflareAccountsNotFoundError(InfrastructureError):
	"""Аккаунты не найдены"""
	error_code = "cloudflare_accounts_not_found_error"

	def __init__(self, api_key: str | None = None, **kwargs):
		message = f"No accounts found for this API key"
		# details = {"api_key": api_key}
		super().__init__(message, **kwargs)

class CloudflareServiceError(ExternalServiceError):
	"""Cloudflare service error"""
	error_code = "cloudflare_service_error"

	def __init__(self, message: str, details: dict | None = None, **kwargs):
		service = "Cloudflare"
		details = details if isinstance(details, dict) else {}
		super().__init__(service=service, message=message, details=details, **kwargs)

class NSIsNotListError(InfrastructureError):
	"""NS не в формате List[str]"""
	error_code = "ns_is_not_list_error"

	def __init__(self, ns: str, **kwargs):
		message = f"NS is not List[str]: {ns}"
		details = {"ns": ns}
		super().__init__(message, details=details, **kwargs)
