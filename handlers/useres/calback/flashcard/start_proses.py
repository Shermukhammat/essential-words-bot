from loader import dp, db, bot
from aiogram import types
from utilites.buttons import InlineButtons, DefoltButton
from utilites.states import UserState
from utilites import shoud_edit, get_semaphore, get_expair_time
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta, timezone
from asyncio import Semaphore

start_progres_semaphore = Semaphore()

@dp.callback_query_handler(state=UserState.flashcard.start_progress)
async def start_flashcard_calback(query : types.CallbackQuery, state : FSMContext):
    async with start_progres_semaphore:
        state_data = await state.get_data()
    
        if query.data == 'back':
            book = state_data.get('book')
            await state.set_state(UserState.flashcard.get_units)

            if shoud_edit(query.message.date):
                await query.message.edit_text(text=f"📖 Book: {book} flashcard \nUnitlarni tanlang, maksimal 5ta unit 👇",
                                          reply_markup=InlineButtons.unit_buttons(state_data.get('selected', []), book = book))
            else:
                await query.message.answer(f"📖 Book: {book} flashcard \nUnitlarni tanlang, maksimal 5ta unit 👇",
                                       reply_markup=InlineButtons.unit_buttons(state_data.get('selected', []), book = book))
                await query.message.delete()
        
        elif query.data == 'cancle':
            await state.reset_state()

            await query.message.answer("✅ Flashcard bekor qilndi", reply_markup=DefoltButton.user_home_menu)
            await query.message.delete()
        
        elif query.data == 'start':
            await start_flashcard(query, state)

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
            await query.answer("❌ Noto'g'ri buyruq", show_alert=True)


async def edit_start_message(query : types.CallbackQuery, state_data : dict):
    selected = str(state_data.get('selected'))
    order = state_data.get('order', 'uzen')
    book = state_data.get('book')
    random = state_data.get('random')
    random_text, uzen_text = get_texts(order, random)
        
    if shoud_edit(query.message.date):
        await query.message.edit_text(text = f"📖 Book {book} flashcard \n\n🔢 Unitlar: `{selected[1:-1]}` \n🎲 Aralashtirish: `{random_text}` \n{uzen_text}",
                                         parse_mode=types.ParseMode.MARKDOWN,
                                         reply_markup=InlineButtons.start_flashcard_buttons(order = order,
                                                                                       random = random))
    else:
        await query.message.answer(f"📖 Book {book} flashcard \n\n🔢 Unitlar: `{selected[1:-1]}` \n🎲 Aralashtirish: `{random_text}` \n{uzen_text}",
                                    parse_mode=types.ParseMode.MARKDOWN,
                                    reply_markup=InlineButtons.start_flashcard_buttons(order = order, 
                                                                                  random = random))
            

def get_texts(order : str, random : bool):
    if random:
        random_text = 'yoniq'
    else:
        random_text = 'o\'chiq'
    
    if order == 'defeng':
        uzen_text = "❓ Savol: `🛡 Definiton` \n✅ Javob: `🇬🇧 Inglizcha`"
    elif order == 'defuz':
        uzen_text = "❓ Savol: `🛡 Definiton` \n✅ Javob: `🇺🇿 O'zbekcha`"
    elif order == 'uzen':
        uzen_text = "❓ Savol: `🇺🇿 O'zbekcha` \n✅ Javob: `🇬🇧 Inglizcha`"
    else:
        uzen_text = "❓ Savol: `🇬🇧 Inglizcha` \n✅ Javob: `🇺🇿 O'zbekcha`"
    
    return random_text, uzen_text


import asyncio
from utilites import Flashcards, Card

async def start_flashcard(query : types.CallbackQuery, state : FSMContext):
    await state.set_state(UserState.flashcard.in_progres)
    await query.message.edit_reply_markup()
 
    state_data = await state.get_data()
    book = state_data.get('book', 1)
    units = [await db.get_unit(book, unit) for unit in state_data.get('selected', [])]
    
    flashcards = Flashcards(book=book, 
                units=units, 
                order=state_data.get('order', 'enuz'),
                mix = state_data.get('random'))


    message_data = await query.message.answer("Flashcardni boshlashga tayyormisiz ?")
    await asyncio.sleep(1)
    await message_data.delete()
    await message_data.answer("🚀", reply_markup=DefoltButton.user_test_buttons)
    await asyncio.sleep(2)
        

    card = flashcards.get_card()
    message = await query.message.answer(f"[{card.num}/{flashcards.length}] \n❓ Savol: {card.value}", 
                               reply_markup=InlineButtons.flashcard_buttons)
    
    await state.update_data(card = card, 
                            flashcards = flashcards, 
                            start = datetime.now(), 
                            message_id = message.message_id)    


    