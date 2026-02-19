from fastapi import APIRouter, Depends

from . import schemas
from .dependencies import get_cloudflare_get_verify_link, get_cloudflare_write_account_data, get_cloudflare_generate_ns
from src.application.cloudflare.use_cases.get_verify_link import CloudflareGetVerifyLink
from src.application.cloudflare.use_cases.write_account_data import CloudflareWriteAccountData
from src.application.cloudflare.use_cases.generate_ns import CloudflareGenerateNS
from src.application.cloudflare.commands import CloudflareGetVerifyLinkCommand, CloudflareWriteAccountDataCommand, CloudflareGenerateNSCommand

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

@router.post("/generate_ns") # response_model=schemas.CloudflateAccountNSResponse
async def cloudflare_generate_ns(
	request: schemas.CloudflareGenerateNSRequest,
	cloudflare_generate_ns: CloudflareGenerateNS = Depends(get_cloudflare_generate_ns)
):
	command = CloudflareGenerateNSCommand(domain=request.domain, ip=request.ip)
	cloudflare_ns = await cloudflare_generate_ns.execute(command)
	if cloudflare_ns:
		return schemas.CloudflateAccountNSResponse.model_validate(cloudflare_ns.model_dump())
