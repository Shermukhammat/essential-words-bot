from loader import dp, db, bot
from aiogram import types
from utilites.buttons import InlineButtons, DefoltButton
from utilites.states import UserState
from utilites import shoud_edit, get_semaphore, get_expair_time
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
        
        elif query.data == 'cancle':
            await state.reset_state()

            await query.message.answer("✅ Test bekor qilndi", reply_markup=DefoltButton.user_home_menu)
            await query.message.delete()
        
        elif query.data == 'start':
            await start_test(query, state)

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

        elif query.data == 'enuz':
            if state_data.get('order') != 'uzen':
                state_data['order'] = 'uzen'
                await state.update_data(order = 'uzen')
                await edit_start_message(query, state_data)
        
        elif query.data == 'uzen':
            if state_data.get('order') != 'defeng':
                state_data['order'] = 'defeng'
                await state.update_data(order = 'defeng')
                await edit_start_message(query, state_data)

        elif query.data == 'defeng':
            if state_data.get('order') != 'defuz':
                state_data['order'] = 'defuz'
                await state.update_data(order = 'defuz')
                await edit_start_message(query, state_data)

        elif query.data == 'defuz':
            if state_data.get('order') != 'enuz':
                state_data['order'] = 'enuz'
                await state.update_data(order = 'enuz')
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
    # uzen = state_data.get('uzen')
    order = state_data.get('order', 'uzen')
    book = state_data.get('book')
    time = state_data.get('time')
    random = state_data.get('random')
    random_text, uzen_text = get_texts(order, random)
        
    if shoud_edit(query.message.date):
        await query.message.edit_text(text = f"📖 Book {book} Test\n \n🔢 Unitlar: `{selected[1:-1]}` \n⏳ Vaxt harbir test uchun: `{time} sec` \n🎲 Aralashtirish: `{random_text}` \n{uzen_text}",
                                         parse_mode=types.ParseMode.MARKDOWN,
                                         reply_markup=InlineButtons.start_test_buttons(order = order,
                                                                                       random = random, 
                                                                                       time = time))
    else:
        await query.message.answer(f"📖 Book {book} Test\n \n🔢 Unitlar: `{selected[1:-1]}` \n⏳ Vaxt harbir test uchun: `{time} sec` \n🎲 Aralashtirish: `{random_text}` \n{uzen_text}",
                                    parse_mode=types.ParseMode.MARKDOWN,
                                    reply_markup=InlineButtons.start_test_buttons(order = order, 
                                                                                  random = random, 
                                                                                  time = time))
            

def get_texts(order : str, random : bool):
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
    
    return random_text, uzen_text


import asyncio
from utilites import Test

async def start_test(query : types.CallbackQuery, state : FSMContext):
    await state.set_state(UserState.test.in_progres)
    await query.message.edit_reply_markup()

    state_data = await state.get_data()
    book = state_data.get('book', 1)
    units = [await db.get_unit(book, unit) for unit in state_data.get('selected', [])]
    
    test = Test(book=book, 
                units=units, 
                order=state_data.get('order', 'enuz'),
                mix = state_data.get('random'),
                time=state_data.get('time', 30))


    message_data = await query.message.answer("Testni boshlashga tayyormisiz ?")
    await asyncio.sleep(1)
    await message_data.edit_text("🚀")
    await asyncio.sleep(2)
    await message_data.delete()

    question = test.get_question()

    pool_data = await query.message.answer_poll(f"[{question.num}/{test.length}] {question.value}",
                                    is_anonymous=False,
                                    explanation=f"To'gri javob `{question.answer}` edi",
                                    explanation_parse_mode=types.ParseMode.MARKDOWN,
                                    options = question.options,
                                    correct_option_id = question.answer_index,
                                    open_period=test.time,
                                    reply_markup=DefoltButton.user_test_buttons,
                                    type='quiz')
    
    await state.update_data(current_question = question, 
                            test = test, 
                            start = datetime.now(), 
                            message_id = pool_data.message_id, 
                            poll_id = pool_data.poll.id)    


    