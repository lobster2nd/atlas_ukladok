from aiogram.fsm.state import StatesGroup, State


class PlacementAdd(StatesGroup):
    title = State()
    content = State()
    video_link = State()
    publish = State()