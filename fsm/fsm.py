from aiogram.fsm.state import State, StatesGroup


class Request(StatesGroup):
    services = State()
    description = State()
    deadlines = State()
    communication = State()
    phone = State()
    confirmation = State()
