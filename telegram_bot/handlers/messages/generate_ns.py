import logging
from typing import List
from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import httpx

from core.config import settings
from schemas.user import User
from schemas.domain_ip_pair import DomainIPPair
from states.user import StateGenerateNS
from utils.i18n import i18n

logger = logging.getLogger()

router = Router()

@router.message(F.chat.type == "private", F.text, StateGenerateNS.message)
async def handle_state_message(message: Message, state: FSMContext, bot: Bot, user: User):
	text = message.text
	pairs: List[DomainIPPair] = []

	try:
		lines = text.split("\n")

		for i, line in enumerate(lines, 1):
			line = line.strip()
			if not line:
				continue

			if ':' not in line:
				logger.error(f"Строка {i}: нет разделителя ':'")
				continue

			domain, ip = line.split(":", 1)
			domain = domain.strip()
			ip = ip.strip()

			try:
				pair = DomainIPPair(domain=domain, server_ip=ip)
				pairs.append(pair)
			except ValueError as e:
				logger.error(f"Строка {i}: {str(e)}")

	except Exception as e:
		text = f"Ошибка: {str(e)}"
		# text = i18n.translate(namespace="responses.email", key="errors.invalid.message", lang=user.language_code)
		return await message.answer(text=text)

	print("pairs:", pairs)
	if not pairs:
		return await message.answer("❌ Нет корректных данных.\nПовторите еще раз в формате <code>domain:server_ip</code>")

	await state.clear()
	await message.answer("⌛️ Задача в работе, ожидайте...")

	# Вынести в отдельный файл
	print("Полученные данные:", pairs)

	client = httpx.AsyncClient(timeout=60)
	data = []

	for pair in pairs:
		params = {"domain": pair.domain, "ip": pair.server_ip}
		url = f"https://{settings.api_domain}/api/v1/cloudflare/generate_ns"
		try:
			response = await client.post(url, json=params)
			cloudflare_data = response.json()
			if cloudflare_data:
				data.append(cloudflare_data)
		except Exception as e:
			logger.error("Cloudflare ns not found")

	print("data [cloudflare_data]:", data)

	text = ""
	for i in data:
		if isinstance(i, dict):
			ns_text = ";".join(i["ns"])
			text += f"<code>{i['email']};{i['password']};{ns_text}</code>\n"

	if not text:
		return await message.answer("Данные не обработаны!, необходимо добавить ретраи и увеличить таймауты запросов.")

	await message.answer(text)
