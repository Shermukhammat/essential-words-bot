from loader import db, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from utilites.states.useres import UserState
from utilites.buttons import DefoltButton
import re


books = ["📗", "📕", "📘", "📙", "📔", "📓"]

@dp.message_handler(state=UserState.book_menu)
async def book_menu_handler(update : types.Message, state : FSMContext):
    
    if update.text == "⬅️ Orqaga":
        await state.finish()

        await update.answer("🎛 Bosh menu", reply_markup=DefoltButton.user_home_menu)


    elif re.search(r'Unit\s(30|[1-9]|[12][0-9])\b', update.text):
        state_data = await state.get_data()
        book_num = state_data.get('book', 1)
        unit = int(update.text[-2:])

        await state.update_data(unit = unit)
        await state.set_state(UserState.unit_menu)
        
        await update.answer(f"{books[book_num-1]} Unit {unit} menu", reply_markup=DefoltButton.get_unit_menu(unit = unit, book = book_num))
        
    else:
        state_data = await state.get_data()
        book_num = state_data.get('book', 1)

        await update.answer("❌ Noto'gri buyruq", 
                            reply_markup = DefoltButton.get_book_menu(book_num))