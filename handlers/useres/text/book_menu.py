from loader import db, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from utilites.states.useres import UserState
from utilites.buttons import DefoltButton



@dp.message_handler(state=UserState.book_menu)
async def book_menu_handler(update : types.Message, state : FSMContext):
    
    if update.text == "⬅️ Orqaga":
        await state.finish()

        await update.answer("🎛 Bosh menu", reply_markup=DefoltButton.user_home_menu)

    else:
        state_data = await state.get_data()
        book_num = state_data.get('book', 1)

        await update.answer("❌ Noto'gri buyruq", 
                            reply_markup = DefoltButton.get_book_menu(book_num))