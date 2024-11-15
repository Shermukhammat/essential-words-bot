from loader import dp, db, bot
from utilites.states.useres import UserState
from utilites.buttons import DefoltButton, InlineButtons
from utilites import shoud_edit, get_semaphore, Test, Question
from aiogram.dispatcher import FSMContext
from aiogram import types
from datetime import datetime


@dp.message_handler(state=UserState.test.in_progres)
async def in_progres_tes_text(update : types.Message, state : FSMContext):
    semaphore = await get_semaphore(state)
    if not semaphore:
        return
    
    async with semaphore:
        if update.text == "➡️ Keyingi":
            state_data = await state.get_data()     

            question : Question = state_data.get('current_question')
            test : Test = state_data.get('test') 
            test.add_answer(question)        
            question = test.get_question()

            if question:
                pool_data = await update.answer_poll(f"[{question.num}/{test.length}] {question.value}",
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
                                        message_id = pool_data.message_id,
                                        poll_id = pool_data.poll.id)

            else:
                start_time : datetime = state_data.get('start')
                test.total_time = (datetime.now() - start_time).seconds
                
                await state.reset_state()
                await update.answer(test.get_resolts(),
                                    reply_markup=DefoltButton.user_home_menu)


        elif update.text == "❌ Bekor qilish":
            await state.reset_state()
            await update.answer("✅ Test bekor qilndi", reply_markup=DefoltButton.user_home_menu)
        
        else:
            await update.answer("❌ Noto'gri buyruq, quydagi tugmalrdan birini bosing", 
                                reply_markup=DefoltButton.user_test_buttons)
        
