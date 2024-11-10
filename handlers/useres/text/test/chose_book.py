from loader import dp, db, bot
from utilites.states.useres import UserState
from utilites.buttons import DefoltButton, InlineButtons
from aiogram.dispatcher import FSMContext
from aiogram import types

books_icon = {1:"📗", 2:"📕", 3:"📘", 4:"📙", 5:"📔", 6:"📓"}

@dp.message_handler(state=UserState.test.get_book_num)
async def test_handler(update : types.Message, state : FSMContext):
    await update.answer("❌ Iltimos kitobni tanlang yoki bekor qilish tugmasni bosing", reply_markup=InlineButtons.books_button)
        