from aiogram.dispatcher.filters.state import State, StatesGroup




class TestState(StatesGroup):
    get_book_num = State()
    get_units = State()
    get_words_order  = State()
    start_test = State()
    in_progres = State()


class UserState(StatesGroup):
    book_menu = State()
    unit_menu = State()

    test = TestState()
