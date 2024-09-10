from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

KEYWORDS = ['Голова', 'Позвоночник', 'Конечности', 'Грудь', 'Живот',
            'Весь список']

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=KEYWORDS[0]), KeyboardButton(text=KEYWORDS[1])],
    [KeyboardButton(text=KEYWORDS[2]), KeyboardButton(text=KEYWORDS[3])],
    [KeyboardButton(text=KEYWORDS[4]), KeyboardButton(text=KEYWORDS[5])],
], resize_keyboard=True)

finish_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Завершить загрузку')]
], resize_keyboard=True)

body_parts_inline_kb = InlineKeyboardBuilder()
for part in KEYWORDS[:5]:
    body_parts_inline_kb.row(InlineKeyboardButton(text=part,
                                                  callback_data=part))

yes_no_kb = InlineKeyboardBuilder()
yes_no_kb.button(text="Да", callback_data="да")
yes_no_kb.button(text="Нет", callback_data="нет")
yes_no_kb.row()
