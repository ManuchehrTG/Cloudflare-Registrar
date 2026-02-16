from fastapi import APIRouter, Depends

from . import schemas
from src.api.v1.imap.dependencies import get_cloudflare_get_verify_link
from src.application.imap.use_cases.cloudflare_get_verify_link import CloudflareGetVerifyLink
from src.application.imap.commands import CloudflareGetVerifyLinkCommand

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/cloudflare/verify_link", response_model=schemas.CloudflareVerifyLinkResponse)
async def get_cloudflare_verify_link(
	request: schemas.CloudflareGetVerifyLinkRequest,
	cloudflare_get_verify_link: CloudflareGetVerifyLink = Depends(get_cloudflare_get_verify_link)
):
	command = CloudflareGetVerifyLinkCommand(email=request.email, password=request.password, proxy=request.proxy)
	cf_verify_link_dto = await cloudflare_get_verify_link.execute(command)
	return schemas.CloudflareVerifyLinkResponse.from_orm(cf_verify_link_dto)
