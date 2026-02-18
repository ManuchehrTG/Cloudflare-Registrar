from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards import BaseCallbackData
from keyboards.templates import TemplatesInlineKeyboard
from schemas.user import User
from states.user import StateGenerateNS
from utils.i18n import i18n
from utils.telegram import SafeMessage

router = Router()

@router.callback_query(F.message.chat.type == "private", BaseCallbackData.filter((F.role == "user") & (F.action == "generate_ns")), StateFilter(None))
async def handle_generate_ns(call: CallbackQuery, callback_data: TemplatesInlineKeyboard, state: FSMContext, bot: Bot, user: User):
	await SafeMessage.message_delete(message=call.message)

	text: str = i18n.translate(namespace="responses.generate_ns", key="message", lang=user.language_code)

	await call.message.answer(text=text)
	await state.set_state(StateGenerateNS.message)
