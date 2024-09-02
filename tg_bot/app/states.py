from aiogram.fsm.state import StatesGroup, State


class PlacementAdd(StatesGroup):
    body_part = State()
    title = State()
    content = State()
    video_link = State()
    publish = State()
    image = State()