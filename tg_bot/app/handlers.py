import requests

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from dotenv import load_dotenv

load_dotenv()

router = Router()

KEYWORDS = ['Голова', 'Позвоночник', 'Конечности', 'Грудь', 'Живот']

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=KEYWORDS[0]), KeyboardButton(text=KEYWORDS[1])],
    [KeyboardButton(text=KEYWORDS[2]), KeyboardButton(text=KEYWORDS[3])],
    [KeyboardButton(text=KEYWORDS[4])]
], resize_keyboard=True)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Какая укладка вас интересует?',
                         reply_markup=main_kb
                         )


@router.message(F.text.in_(KEYWORDS))
async def request_head(message: Message):
    url = 'http://127.0.0.1:8000/api/v1/atlas/placement/'
    response = requests.get(url).json()
    placements = [p['title'] for p in response]

    await message.answer(f'Есть такие укладки: {", ".join(placements)}')
