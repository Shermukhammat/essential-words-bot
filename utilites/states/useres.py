from aiogram.dispatcher.filters.state import State, StatesGroup




class UserState(StatesGroup):
    book_menu = State()
    