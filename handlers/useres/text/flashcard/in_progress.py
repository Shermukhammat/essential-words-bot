from loader import dp, db, bot, flashcard_progress
from utilites.states.useres import UserState
from utilites.buttons import DefoltButton, InlineButtons
from utilites import shoud_edit, get_semaphore, Flashcards, Card
from aiogram.dispatcher import FSMContext
from aiogram import types
from datetime import datetime


@dp.message_handler(state=UserState.flashcard.in_progres)
async def in_progres_flashcard_text(update : types.Message, state : FSMContext):
    async with flashcard_progress:
        if update.text == "❌ Bekor qilish":
            await state.reset_state()
            await update.answer("✅ Flashcard bekor qilndi", reply_markup=DefoltButton.user_home_menu)
        
        elif update.text == "➡️ Keyingi":
            state_data = await state.get_data()
            flashcards : Flashcards  = state_data.get('flashcards')
            card : Card = state_data.get('card')
            message_id = state_data.get('message_id')

            flashcards.cards.append(card)
            card = flashcards.get_card()

            try:
                await bot.delete_message(chat_id=update.from_user.id, message_id=message_id)
            except:
                pass

            message_data = await update.answer(f"[{card.num}/{flashcards.length}] \n❓ Savol: {card.value}",
                                           reply_markup=InlineButtons.flashcard_buttons)
            await state.update_data(card = card, flashcards = flashcards, message_id = message_data.message_id)
        
        else:
            await update.answer("❌ Noto'gri buyruq, quydagi tugmalrdan birini bosing", 
                                reply_markup=DefoltButton.user_test_buttons)
        
