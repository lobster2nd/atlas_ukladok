import os

import aiohttp


async def form_payload(data: dict) -> dict:
    """Формирование данных для POST запроса о добавлении укладки"""
    payload = {
        'title': data.get('title'),
        'body_part': data.get('body_part'),
        'content': data.get('content'),
        'video_link': data.get('video_link') if data.get('video_link') else None,
        'tg_user': data.get('tg_user')
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
            response_data = await response.json()
    return response_data


async def send_image_data(images, placement_id):
    """Отправка запроса на добавление изображения к укладке"""
    url = os.getenv('IMAGE_ADD_URL')
    async with aiohttp.ClientSession() as session:
        responses = []
        form_data = aiohttp.FormData()
        for image in images:
            form_data.add_field('placement', placement_id)
            form_data.add_field('photo', image,
                                filename=f'image{placement_id}.jpg',
                                content_type='image/jpeg')
        async with session.post(url=url, data=form_data) as response:
            response_data = await response.json()
            responses.append(response_data)
            return responses
