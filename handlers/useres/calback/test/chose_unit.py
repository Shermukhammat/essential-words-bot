from loader import dp, db, bot
from aiogram import types
from utilites.buttons import InlineButtons, DefoltButton
from utilites.states import UserState
from utilites import shoud_edit, get_semaphore
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta, timezone
from asyncio import Semaphore

chose_unit_semaphore = Semaphore(1)
books_icon = {1:"📗", 2:"📕", 3:"📘", 4:"📙", 5:"📔", 6:"📓"}

@dp.callback_query_handler(state = UserState.test.get_units)
async def get_unit_num_calback(query : types.CallbackQuery, state : FSMContext):
    semaphore = await get_semaphore(state)
    async with semaphore:
        if query.data == 'cancle':
            await state.reset_state()
            await query.message.answer("✅ Test bekor qilndi", reply_markup=DefoltButton.user_home_menu)

            await query.message.delete()
    
        elif query.data == 'back':
            await state.set_state(UserState.test.get_book_num)

            if shoud_edit(query.message.date):
                await query.message.edit_text(text="Kitobni tanlang 👇", reply_markup=InlineButtons.books_button)
            else:
                await query.message.answer("Kitobni tanlang 👇", reply_markup=InlineButtons.books_button)
                await query.message.delete()
    
        elif query.data == 'next':
            state_data = await state.get_data()
            selected : list[int] = state_data.get('selected', [])

            if selected:
                await go_next_state(query, state, state_data=state_data)
            else:
                await query.answer("❌ Noto'g'ri buyruq", cache_time=60)

        else:
            command, unit = get_unit(query.data)
            if command:
                await update_unit(query, state, command=command, unit = unit)
            
            else:
                await query.answer("❌ Noto'g'ri buyruq", cache_time=60)


async def go_next_state(query : types.CallbackQuery, state : FSMContext, state_data : dict = None):
    book = state_data.get('book')
    selected = str(state_data.get('selected', []))
    order = state_data.get('order', 'uzen')
    random = state_data.get('random')
    await state.set_state(UserState.test.start_test)

    if random:
        random_text = 'yoniq'
    else:
        random_text = 'o\'chiq'
    
    if order == 'defeng':
        uzen_text = "❓ Savol: `🛡 Definiton` \n🧩Variyantlar: `🇬🇧 Inglizcha`"
    elif order == 'defuz':
        uzen_text = "❓ Savol: `🛡 Definiton` \n🧩Variyantlar: `🇺🇿 O'zbekcha`"
    elif order == 'uzen':
        uzen_text = "❓ Savol: `🇺🇿 O'zbekcha` \n🧩Variyantlar: `🇬🇧 Inglizcha`"
    else:
        uzen_text = "❓ Savol: `🇬🇧 Inglizcha` \n🧩Variyantlar: `🇺🇿 O'zbekcha`"
    
    if shoud_edit(query.message.date):
        await query.message.edit_text(text = f"📖 Book {book} Test \n\n🔢 Unitlar: `{selected[1:-1]}` \n⏳ Vaxt harbir test uchun: `{state_data.get('time')} sec` \n🎲 Aralashtirish: `{random_text}` \n{uzen_text}",
                                         parse_mode=types.ParseMode.MARKDOWN,
                                         reply_markup=InlineButtons.start_test_buttons(order = order,
                                                                                       random = random,
                                                                                       time = state_data.get('time')))
    else:
        await query.message.answer(f"📖 Book: {book} Test \n🔢 Unitlar: `{selected[1:-1]}` \n⏳ Vaxt harbir test uchun: `{state_data.get('time')} sec` \n🎲 Aralashtirish: `{random_text}` \n{uzen_text}",
                                    parse_mode=types.ParseMode.MARKDOWN,
                                    reply_markup=InlineButtons.start_test_buttons(order = order,random = random, time = state_data.get('time')))


async def update_unit(query : types.CallbackQuery, state : FSMContext, command : str = 's', unit : int = 1):
    async with chose_unit_semaphore:
        state_data = await state.get_data()
        selected : list[int] = state_data.get('selected', [])
        book : int = state_data.get('book', 1)

        if command == 's': #selected unit
            if len(selected) >= 5:
                await query.answer("❌ Unitlar soni 5tadan ko'p bo'lishi mumkun emas", show_alert=True)
            
            elif unit not in selected:
                selected.append(unit)
                await state.update_data(selected = selected)
                await query.message.edit_reply_markup(InlineButtons.unit_buttons(selected, book = book))
            
        elif command == 'u': #unselect item
            if unit in selected:
                selected.remove(unit)
                await state.update_data(selected = selected)

                await query.message.edit_reply_markup(InlineButtons.unit_buttons(selected, book = book))


def get_unit(query : str) -> tuple[str, int]:
    if len(query) > 1 and query[1:].isnumeric():
        return query[0], int(query[1:])
    return None, None 
    

