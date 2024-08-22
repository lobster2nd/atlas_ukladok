import os

import aiohttp

from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from dotenv import load_dotenv

load_dotenv()

router = Router()

KEYWORDS = ['Голова', 'Позвоночник', 'Конечности', 'Грудь', 'Живот',
            'Весь список']

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=KEYWORDS[0]), KeyboardButton(text=KEYWORDS[1])],
    [KeyboardButton(text=KEYWORDS[2]), KeyboardButton(text=KEYWORDS[3])],
    [KeyboardButton(text=KEYWORDS[4]), KeyboardButton(text=KEYWORDS[5])]
], resize_keyboard=True)


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Стартовое меню с выбором анатомической области"""
    await message.answer('Какая укладка вас интересует?',
                         reply_markup=main_kb
                         )


@router.message(F.text.in_(KEYWORDS))
async def request_placements(message: Message):
    """Запрос списка укалдок выбранной категории"""

    url = os.getenv('PLACEMENTS_URL')

    match message.text:
        case 'Голова':
            url += '?body_part=head'
        case 'Позвоночник':
            url += '?body_part=spine'
        case 'Конечности':
            url += '?body_part=limbs'
        case 'Грудь':
            url += '?body_part=thorax'
        case 'Живот':
            url += '?body_part=abdomen'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_data = await response.json()
    placements = [p for p in response_data]

    builder = InlineKeyboardBuilder()
    for placement in placements:
        builder.button(text=placement['title'],
                       callback_data=str(placement['id']))

    await message.answer('Есть такие укладки:',
                         reply_markup=builder.as_markup())


@router.callback_query(lambda c: True)
async def handle_placement_selection(callback_query: types.CallbackQuery):
    """В ответ на выбранную укладку возвращается текст и изображение"""

    url = os.getenv('PLACEMENTS_URL') + f'{callback_query.data}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_data = await response.json()
    await callback_query.message.answer(text=response_data['content'])

    if response_data['images']:
        media_url = os.getenv('MEDIA_URL')
        img_list = [media_url + i['photo'] for i in response_data['images']]
        images = '\n'.join(img_list)
        await callback_query.message.answer(f'Иллюстрации: {images}')
