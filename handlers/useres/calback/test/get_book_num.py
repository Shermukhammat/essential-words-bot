from loader import dp, db, bot
from aiogram import types
from utilites.buttons import InlineButtons, DefoltButton
from utilites import shoud_edit, get_semaphore
from utilites.states import UserState
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta, timezone



@dp.callback_query_handler(state = UserState.test.get_book_num)
async def get_book_num_calback(query : types.CallbackQuery, state : FSMContext):
    semaphore = await get_semaphore(state)
    async with semaphore:
        if query.data.isnumeric() and int(query.data) <= 6 and int(query.data) >= 1:
            await state.update_data(book = int(query.data))
            await UserState.test.next()
            state_data = await state.get_data()

            if shoud_edit(query.message.date):
                await query.message.edit_text(text=f"📖 Book {query.data} Test \nUnitlarni tanlang, maksimal 5ta unit 👇",
                                          reply_markup=InlineButtons.unit_buttons(state_data.get('selected', []), book = int(query.data)))
            else:
                await query.message.answer(f"📖 Book {query.data} Test \nUnitlarni tanlang, maksimal 5ta unit 👇",
                                       reply_markup=InlineButtons.unit_buttons(state_data.get('selected', []), book = int(query.data)))
                await query.message.delete()
        
        elif query.data == 'cancle':
            await state.reset_state()
            await query.message.answer("✅ Test bekor qilndi", reply_markup=DefoltButton.user_home_menu)
            await query.message.delete()

        else:
            await query.answer("❌ Noto'g'ri buyruq", cache_time=60)