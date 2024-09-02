import os

import aiohttp

from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
import logging

from django.template.defaultfilters import title

from .states import PlacementAdd

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = Router()

KEYWORDS = ['Голова', 'Позвоночник', 'Конечности', 'Грудь', 'Живот',
            'Весь список']

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=KEYWORDS[0]), KeyboardButton(text=KEYWORDS[1])],
    [KeyboardButton(text=KEYWORDS[2]), KeyboardButton(text=KEYWORDS[3])],
    [KeyboardButton(text=KEYWORDS[4]), KeyboardButton(text=KEYWORDS[5])],
], resize_keyboard=True)

body_parts_inline_kb = InlineKeyboardBuilder()
for part in KEYWORDS[:5]:
    body_parts_inline_kb.button(text=part, callback_data=part)
    body_parts_inline_kb.row()

yes_no_kb = InlineKeyboardBuilder()
yes_no_kb.button(text="Да", callback_data="да")
yes_no_kb.button(text="Нет", callback_data="нет")
yes_no_kb.row()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Стартовое меню с выбором анатомической области"""
    await message.answer('Какая укладка вас интересует?',
                         reply_markup=main_kb
                         )


@router.message(Command('add', prefix='/'))
async def add_placement(message: Message, state: FSMContext):
    """Обработка запроса на добавление укладки"""
    await state.set_state(PlacementAdd.body_part)
    await message.answer('Выберете анатомическую область',
                         reply_markup=body_parts_inline_kb.as_markup())


@router.callback_query(lambda c: c.data in KEYWORDS)
async def handle_body_part_selection(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    """Обработка выбора области"""
    selected_part = callback_query.data
    await state.update_data(body_part=selected_part)
    await state.set_state(PlacementAdd.title)
    await callback_query.answer()
    await callback_query.message.answer(f'Вы выбрали: {selected_part} \n'
                                        f'Введите название укладки')


@router.message(PlacementAdd.title, F.text)
async def handle_add_title(message: Message, state: FSMContext):
    """Обработка введённого названия укладки"""
    await state.update_data(title=message.text)
    await state.set_state(PlacementAdd.content)
    await message.answer('Введите текст')


@router.message(PlacementAdd.content, F.text)
async def handle_add_placement(message: Message, state: FSMContext):
    """Обработка текста укладки"""
    await state.update_data(content=message.text)
    await message.answer('Хотите добавить ссылку на видео?',
                         reply_markup=yes_no_kb.as_markup())


async def form_payload(data: dict) -> dict:
    """Формирование данных для POST запроса о добавлении укладки"""
    payload = {
        'title': data.get('title'),
        'body_part': data.get('body_part'),
        'content': data.get('content'),
        'video_link': data.get('video_link') if data.get('video_link') else None
    }
    match data.get('body_part'):
        case 'Голова':
            payload['body_part'] = 'head'
        case 'Позвоночник':
            payload['body_part'] = 'spine'
        case 'Конечности':
            payload['body_part'] = 'limbs'
        case 'Грудь':
            payload['body_part'] = 'thorax'
        case 'Живот':
            payload['body_part'] = 'abdomen'
    return payload


async def send_placement_data(data: dict):
    """Отправка запроса на добавление укладки"""
    url = os.getenv('PLACEMENTS_URL')
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=data) as response:
            await response.json()
    return response.status


@router.callback_query(lambda c: c.data in ["да", "нет"])
async def handle_vido_link_confirmation(callback_query: types.CallbackQuery,
                                        state: FSMContext):
    """Вопрос пользователю о добавлении ссылки на видео"""
    await callback_query.answer()
    if callback_query.data == 'нет':
        await state.update_data(video_link=None)
        data = await state.get_data()
        payload = form_payload(data=data)
        await state.clear()
        result = await send_placement_data(await payload)
        await callback_query.message.answer(str(result))
    else:
        await state.set_state(PlacementAdd.video_link)
        await callback_query.message.answer('Введите ссылку на видео')


@router.message(PlacementAdd.video_link, F.text)
async def handle_video_link(message: Message, state: FSMContext):
    """Обработка ссылки на видео"""
    video_link = message.text
    await state.update_data(video_link=video_link) if video_link else None
    await state.set_state(PlacementAdd.publish)
    await message.answer(f'Ссылка на видео добавлена')
    data = await state.get_data()
    payload = form_payload(data=data)
    await state.clear()
    result = await send_placement_data(await payload)
    await message.answer('Добавление завершено', str(result))


@router.message(F.text.in_(KEYWORDS[:6]))
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
