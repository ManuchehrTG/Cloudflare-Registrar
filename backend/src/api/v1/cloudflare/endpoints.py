from fastapi import APIRouter, Depends

from . import schemas
from .dependencies import get_cloudflare_get_verify_link, get_cloudflare_write_account_data
from src.application.cloudflare.use_cases.cloudflare_get_verify_link import CloudflareGetVerifyLink
from src.application.cloudflare.use_cases.cloudflare_write_account_data import CloudflareWriteAccountData
from src.application.cloudflare.commands import CloudflareGetVerifyLinkCommand, CloudflareWriteAccountDataCommand

router = APIRouter(prefix="/cloudflare", tags=["Cloudflare"])

@router.post("/get_verify_link", response_model=schemas.CloudflareVerifyLinkResponse)
async def get_cloudflare_verify_link(
	request: schemas.CloudflareGetVerifyLinkRequest,
	cloudflare_get_verify_link: CloudflareGetVerifyLink = Depends(get_cloudflare_get_verify_link)
):
	command = CloudflareGetVerifyLinkCommand(email=request.email, password=request.password, proxy=request.proxy)
	cf_verify_link_dto = await cloudflare_get_verify_link.execute(command)
	return schemas.CloudflareVerifyLinkResponse.model_validate(cf_verify_link_dto.model_dump())

@router.post("/account_data", response_model=schemas.CloudflareAccountDataResponse)
async def cloudflare_write_account_data(
	request: schemas.CloudflareAccountDataRequest,
	cloudflare_write_account_data: CloudflareWriteAccountData = Depends(get_cloudflare_write_account_data)
):
	command = CloudflareWriteAccountDataCommand(email=request.email, password=request.password, api_key=request.api_key)
	await cloudflare_write_account_data.execute(command)
	return schemas.CloudflareAccountDataResponse(status="ok")
