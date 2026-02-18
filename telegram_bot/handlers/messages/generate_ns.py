import httpx
import logging
from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message
from datetime import datetime

from core.config import settings
from schemas.user import User
from states.user import StateGenerateNS
from services.domain_ip_pair_parser import DomainIPPairParser
from services.cloudflare import CloudflareService
from utils.i18n import i18n

logger = logging.getLogger()

router = Router()

@router.message(F.chat.type == "private", F.text, StateGenerateNS.message)
async def handle_state_message(message: Message, state: FSMContext, bot: Bot, user: User):
	text: str = message.text

	parser = DomainIPPairParser()
	result = parser.parse(text)

	if result.errors:
		error_text = "Найдены ошибки в следующих строках:\n\n"
		for err in result.errors:
			error_text += f"Строка {err.line_number}: {err.error}\n`{err.raw_line}`\n\n"

		if not result.pairs:
			return await message.answer(
				f"❌ Нет корректных строк:\n\n{error_text}"
			)
		else:
			await message.answer(
				f"⚠️ Частичный успех. Обработано {len(result.pairs)} строк.\n\n{error_text}"
			)

	await state.clear()
	await message.answer(
		f"✅ Получено {len(result.pairs)} пар домен:IP\n"
		f"⌛️ Задача в работе, ожидайте..."
	)

	# ====================================

	# client = httpx.AsyncClient(timeout=60)
	# data = []

	# for pair in result.pairs:
	# 	params = {"domain": pair.domain, "ip": pair.server_ip}
	# 	url = f"https://{settings.api_domain}/api/v1/cloudflare/generate_ns"
	# 	try:
	# 		response = await client.post(url, json=params)
	# 		cloudflare_data = response.json()
	# 		if cloudflare_data.get("email") and cloudflare_data.get("password") and cloudflare_data.get("ns"):
	# 			data.append(cloudflare_data)
	# 		else:
	# 			logger.warning("invalid_data:", cloudflare_data)
	# 	except Exception as e:
	# 		logger.error("Cloudflare ns not found")

	# text = ""
	# for i in data:
	# 	if isinstance(i, dict):
	# 		ns_text = ";".join(i["ns"])
	# 		text += f"<code>{i['email']};{i['password']};{ns_text}</code>\n"

	# if not text:
	# 	return await message.answer("Данные не обработаны!") # Необходимо добавить ретраи и увеличить таймауты запросов.

	# await message.answer(text)


	service = CloudflareService(api_domain=settings.api_domain)
	results = await service.process_batch(result.pairs)

	if not results:
		return await message.answer("Нет данных!")

	filename = f"cloudflare_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

	with open(filename, 'w', encoding='utf-8') as f:
		for res in results:
			if res.success and res.data:
				email = res.data.get("email")
				password = res.data.get("password")
				ns_list = res.data.get("ns", [])
				ns_str = ';'.join(ns_list)

				line = f"{email}:{password}:{ns_str}\n"
				f.write(line)
			else:
				line = f"{res.domain}:{res.ip} - {res.error}\n"
				f.write(line)

	with open(filename, 'rb') as f:
		await message.answer_document(
			document=BufferedInputFile(f.read(), filename=filename),
			caption=f"✅ Обработано {len(results)} доменов"
		)

