from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.callback_data import BaseCallbackData

class TemplatesInlineKeyboard:
	@staticmethod
	def main_menu():
		builder = InlineKeyboardBuilder()
		builder.button(text="Сгенерировать NS(-ы)", callback_data=BaseCallbackData(role="user", action="generate_ns"))
		builder.adjust(1)
		return builder.as_markup()
