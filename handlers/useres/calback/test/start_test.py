from loader import dp, db, bot
from aiogram import types
from utilites.buttons import InlineButtons, DefoltButton
from utilites.states import UserState
from utilites import shoud_edit, get_semaphore
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta, timezone
from asyncio import Semaphore


@dp.callback_query_handler(state=UserState.test.start_test)
async def start_test_calback(query : types.CallbackQuery, state : FSMContext):
    semaphore = await get_semaphore(state)
    async with semaphore:
        state_data = await state.get_data()
    
        if query.data == 'back':
            book = state_data.get('book')
            await state.set_state(UserState.test.get_units)

            if shoud_edit(query.message.date):
                await query.message.edit_text(text=f"📖 Book: {book} \nUnitlarni tanlang, maksimal 5ta unit 👇",
                                          reply_markup=InlineButtons.unit_buttons(state_data.get('selected', []), book = book))
            else:
                await query.message.answer(f"📖 Book: {book} \nUnitlarni tanlang, maksimal 5ta unit 👇",
                                       reply_markup=InlineButtons.unit_buttons(state_data.get('selected', []), book = book))
                await query.message.delete()

        elif query.data == 'start':
            pass

        elif query.data == 'random_on':
            if state_data['random'] == True:
                await query.answer("❌ Noto'g'ri buyruq", show_alert=True)
        
            else:
                state_data['random'] = True
                await state.update_data(random = True)
                await edit_start_message(query, state_data)
    
        elif query.data == 'random_off':
            if state_data['random'] == False:
                await query.answer("❌ Noto'g'ri buyruq", show_alert=True)
        
            else:
                state_data['random'] = False
                await state.update_data(random = False)
                await edit_start_message(query, state_data)

        elif query.data == 'uzen_off':
            if state_data['uzen']:
                state_data['uzen'] = False
                await state.update_data(uzen = False)
                await edit_start_message(query, state_data)
        
        elif query.data == 'uzen_on':
            if state_data['uzen'] == False:
                state_data['uzen'] = True
                await state.update_data(uzen = True)
                await edit_start_message(query, state_data)

        else:
            params = query.data.split('&')  
            if len(params) == 2 and params[0] == 'time' and params[1].isnumeric():
                time = int(params[1])
                if state_data['time'] != time:
                    state_data['time'] = time
                    await state.update_data(time = time)
                    await edit_start_message(query, state_data)
            
                else:
                    await query.answer("❌ Noto'g'ri buyruq", show_alert=True)
            
            else:
                await query.answer("❌ Noto'g'ri buyruq", show_alert=True)

async def edit_start_message(query : types.CallbackQuery, state_data : dict):
    selected = str(state_data.get('selected'))
    uzen = state_data.get('uzen')
    book = state_data.get('book')
    time = state_data.get('time')
    random = state_data.get('random')
    random_text, uzen_text = get_texts(uzen, random)
        
    if shoud_edit(query.message.date):
        await query.message.edit_text(text = f"📖 Book {book} Test\n \n🔢 Unitlar: `{selected[1:-1]}` \n⏳ Vaxt harbir test uchun: `{time} sec` \n🎲 Aralashtirish: `{random_text}` \n🔄 Tartib: `{uzen_text}`",
                                         parse_mode=types.ParseMode.MARKDOWN,
                                         reply_markup=InlineButtons.start_test_buttons(uzen = uzen,
                                                                                       random = random, time = time))
    else:
        await query.message.answer(f"📖 Book {book} Test\n \n🔢 Unitlar: `{selected[1:-1]}` \n⏳ Vaxt harbir test uchun: `{time} sec` \n🎲 Aralashtirish: `{random_text}` \n🔄 Tartib: `{uzen_text}`",
                                    parse_mode=types.ParseMode.MARKDOWN,
                                    reply_markup=InlineButtons.start_test_buttons(uzen = uzen,random = random, time = time))
            

def get_texts(uzen : bool, random : bool):
    if random:
        random_text = 'yoniq'
    else:
        random_text = 'o\'chiq'
    if uzen:
        uzen_text = "🇺🇿 O'zbekchadan  🇬🇧 Inglizchaga"
    else:
        uzen_text = "🇬🇧 Inglizchadan 🇺🇿 O'zbekchaga"
    
    return random_text, uzen_text