from aiogram.dispatcher.filters.state import State, StatesGroup




class UserRegistrState(StatesGroup):
    get_lang = State()