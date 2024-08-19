import os
import requests

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, \
    ReplyKeyboardMarkup, KeyboardButton

from dotenv import load_dotenv

load_dotenv()

router = Router()

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Голова'), KeyboardButton(text='Позвоночник')],
    [KeyboardButton(text='Конечности'), KeyboardButton(text='Грудь')],
    [KeyboardButton(text='Живот')]
], resize_keyboard=True)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Какая укладка вас интересует?',
                         reply_markup=main_kb
                         )


@router.message(F.text == 'Голова')
async def request_head(message: Message):
    url = 'http://127.0.0.1:8000/api/v1/atlas/placement/'
    response = requests.get(url).json()
    placements = [p['title'] for p in response]

    await message.answer(f'Есть такие укладки: {", ".join(placements)}')
