from loader import dp, db, bot, flashcard_progress
from aiogram import types
from utilites.buttons import InlineButtons, DefoltButton
from utilites.states import UserState
from utilites import shoud_edit, get_semaphore, get_expair_time, Flashcards, Card
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta, timezone
from asyncio import Semaphore



@dp.callback_query_handler(state=UserState.flashcard.in_progres)
async def flashcard_progres_calback(query : types.CallbackQuery, state : FSMContext):
    async with flashcard_progress:
        state_data = await state.get_data()

        if query.data == 'see' and query.message.message_id == state_data.get('message_id'):
            card : Card = state_data.get('card')
            flashcards : Flashcards = state_data.get('flashcards')

            if shoud_edit(query.message.date):
                await query.message.edit_text(f"[{card.num}/{flashcards.length}] \n❓ Savol: {card.value} \n✅ Javob: {card.answer}", 
                                              reply_markup=InlineButtons.flashcard_buttons_get_answer)
            
            else:
                await query.message.answer(f"[{card.num}/{flashcards.length}] \n❓ Savol: {card.value} \n✅ Javob: {card.answer}", 
                                              reply_markup=InlineButtons.flashcard_buttons_get_answer)
                await query.message.delete()
                
        elif (query.data == 'correct' or query.data == 'wrong') and query.message.message_id == state_data.get('message_id'):
            card : Card = state_data.get('card')
            flashcards : Flashcards = state_data.get('flashcards')
            if query.data == 'correct':
                card.resolt = True
            else:
                card.resolt = False

            flashcards.add_answer(card)
            card = flashcards.get_card()
            if card:
                await query.message.edit_reply_markup()
                message_data = await query.message.answer(f"[{card.num}/{flashcards.length}] \n❓ Savol: {card.value}",
                                           reply_markup=InlineButtons.flashcard_buttons)
                await state.update_data(card = card, flashcards = flashcards, message_id = message_data.message_id)
            
            else:
                await state.reset_state()
                start_time : datetime = state_data.get('start')
                flashcards.total_time = (datetime.now() - start_time).seconds   

                await query.message.answer(flashcards.get_resolts(), reply_markup=DefoltButton.user_home_menu)
                await query.message.edit_reply_markup()
