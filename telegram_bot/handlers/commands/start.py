from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.templates import TemplatesInlineKeyboard
from schemas.user import User
from utils.i18n import i18n

router = Router()

@router.message(Command("start"), F.chat.type == "private")
async def command_start(message: Message, state: FSMContext, bot: Bot, user: User):
	await state.clear()

	text: str = i18n.translate(namespace="commands.start", key="message", lang=user.language_code)
	reply_keyboard = TemplatesInlineKeyboard.main_menu()

	await message.answer(text=text, reply_markup=reply_keyboard)
