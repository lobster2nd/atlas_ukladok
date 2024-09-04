import os

import aiohttp
from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, ContentType, \
    ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

import logging
from dotenv import load_dotenv

from .keyboards import main_kb, body_parts_inline_kb, yes_no_kb, KEYWORDS, \
    finish_kb
from .states import PlacementAdd
from .utils import form_payload, send_placement_data, send_image_data

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Стартовое сообщение приветствия"""
    await message.answer(f'Добро пожаловать! Выберете интересующую команду\n')
    await cmd_help(message)


@router.message(Command('help', prefix='/'))
async def cmd_help(message: Message):
    """Список команд бота"""
    menu = ('/list - Cписок доступных укладок\n'
            '/add - Добавить новую укладку\n'
            '/help - Показать список команд')
    await message.answer(menu)


@router.message(Command('list', prefix='/'))
async def cmd_list(message: Message):
    """Меню с выбором анатомической области"""
    await message.answer('Какая укладка вас интересует?',
                         reply_markup=main_kb)


@router.message(Command('add', prefix='/'))
async def cmd_add_placement(message: Message, state: FSMContext):
    """Обработка запроса на добавление укладки"""
    await message.answer('Выберете анатомическую область',
                         reply_markup=body_parts_inline_kb.as_markup())
    await state.set_state(PlacementAdd.body_part)


@router.callback_query(lambda c: c.data in KEYWORDS)
async def handle_body_part_selection(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    """Обработка выбора области"""
    selected_part = callback_query.data
    await state.update_data(body_part=selected_part)
    await callback_query.answer()
    await callback_query.message.answer(f'Вы выбрали: {selected_part} \n'
                                        f'Введите название укладки',
                                        reply_markup=ReplyKeyboardRemove())
    await state.set_state(PlacementAdd.title)


@router.message(PlacementAdd.title, F.text)
async def handle_add_title(message: Message, state: FSMContext):
    """Обработка введённого названия укладки"""
    await state.update_data(title=message.text)
    await message.answer('Введите текст')
    await state.set_state(PlacementAdd.content)


@router.message(PlacementAdd.content, F.text)
async def handle_add_placement(message: Message, state: FSMContext):
    """Обработка текста укладки"""
    await state.update_data(content=message.text)
    await message.answer('Хотите добавить ссылку на видео?',
                         reply_markup=yes_no_kb.as_markup())
    await state.set_state(PlacementAdd.video_link)


@router.callback_query(lambda c: c.data in ["да", "нет"])
async def handle_confirmation(callback_query: types.CallbackQuery,
                              state: FSMContext):
    """Обработка подтверждения добавления видео или изображения"""
    await callback_query.answer()

    current_state = await state.get_state()

    if current_state == PlacementAdd.video_link.state:
        if callback_query.data == 'нет':
            await state.update_data(video_link=None)
            data = await state.get_data()
            payload = form_payload(data=data)
            response = await send_placement_data(await payload)
            await state.update_data(placement_id=response['id'])
            await callback_query.message.answer(
                'Данные добавлены\n'
                'Хотите добавить изображение?',
                reply_markup=yes_no_kb.as_markup()
            )
            await state.set_state(PlacementAdd.image_add)
        else:
            await state.set_state(PlacementAdd.video_link)
            await callback_query.message.answer('Введите ссылку на видео')

    elif current_state == PlacementAdd.image_add.state:
        if callback_query.data == 'нет':
            await callback_query.message.answer('Добавление завершено')
            await state.clear()
        else:
            await callback_query.message.answer('Добавьте до 10 изображений')
            await state.update_data(uploaded_images=[])
            await state.set_state(PlacementAdd.image_add)


@router.message(PlacementAdd.video_link, F.text)
async def handle_video_link(message: Message, state: FSMContext):
    """Обработка ссылки на видео"""
    video_link = message.text
    await state.update_data(video_link=video_link) if video_link else None
    data = await state.get_data()
    payload = form_payload(data=data)
    response = await send_placement_data(await payload)
    await state.update_data(placement_id=response['id'])
    await message.answer('Ссылка на видео добавлена\n'
                         'Хотите добавить изображение?',
                         reply_markup=yes_no_kb.as_markup())
    await state.set_state(PlacementAdd.image_add)


@router.message(PlacementAdd.image_add)
async def handle_image(message: Message, state: FSMContext):
    """Добавление изображений"""

    if message.content_type != ContentType.PHOTO:
        await message.answer('Необходимо отправить изображение')
        return

    data = await state.get_data()
    uploaded_images = data.get('uploaded_images', [])

    photo = message.photo[-1]
    file_id = photo.file_id
    file = await message.bot.get_file(file_id)
    image_file = await message.bot.download_file(file.file_path)

    uploaded_images.append(image_file)

    await state.update_data(uploaded_images=uploaded_images)
    await message.answer(f'Изображение добавлено!',
                         reply_markup=finish_kb)
    await state.set_state(PlacementAdd.image_send)


@router.message(PlacementAdd.image_send)
async def finish_upload(message: Message, state: FSMContext):
    """Завершение загрузки изображений"""
    data = await state.get_data()
    uploaded_images = data.get('uploaded_images', [])
    placement_id = str(data.get('placement_id'))

    if not uploaded_images:
        await message.answer('Нет загруженных изображений.')
        await state.set_state(PlacementAdd.image_add)
        return

    elif len(uploaded_images) > 10:
        await message.answer('Не более 10 изображений')
        await state.update_data(uploaded_images=[])
        return

    await send_image_data(uploaded_images, placement_id)
    await message.answer(
        f'Изображения успешно добавлены!',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


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
        builder.row(InlineKeyboardButton(text=placement['title'],
                                         callback_data=str(placement['id'])))

    await message.answer('Есть такие укладки:',
                         reply_markup=builder.as_markup())


@router.callback_query(lambda c: True)
async def handle_placement_selection(callback_query: types.CallbackQuery):
    """В ответ на выбранную укладку возвращается текст и изображение"""

    await callback_query.answer()
    url = os.getenv('PLACEMENTS_URL') + f'{callback_query.data}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_data = await response.json()
    await callback_query.message.answer(text=response_data['content'])

    if response_data['video_link']:
        link = response_data['video_link']
        await callback_query.message.answer(f'Видео: {link}')

    if response_data['images']:
        media_url = os.getenv('MEDIA_URL')
        img_list = [media_url + i['photo'] for i in response_data['images']]
        images = '\n'.join(img_list)
        await callback_query.message.answer(f'Иллюстрации: {images}')
