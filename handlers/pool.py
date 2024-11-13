from aiogram.types import PollAnswer, Poll
from loader import dp, bot, db
from utilites.states import UserState
from utilites.buttons import DefoltButton
from utilites import get_semaphore, Test, Question
from aiogram.dispatcher import FSMContext
from aiogram import types
from datetime import datetime


@dp.poll_answer_handler()
async def handle_poll_answer(poll_answer: PollAnswer):
    user_id = poll_answer.user.id
    if db.is_user(user_id):
        state = dp.current_state(chat=user_id, user=user_id)
        current_state = await state.get_state()
        
        if current_state == UserState.test.in_progres.state:
            semaphore = await get_semaphore(state)
            if not semaphore:
                return
            
            async with semaphore:
                state_data = await state.get_data('current')
                question : Question = state_data.get('current_question')
                test : Test = state_data.get('test')
                poll_id : str = state_data.get('poll_id')

                if poll_answer.poll_id != poll_id:
                    return

                question.check_answer(poll_answer.option_ids[0])
                test.add_answer(question)
                question = test.get_question()

                if question:
                    pool_data = await bot.send_poll(chat_id = poll_answer.user.id,
                                    question = f"[{question.num}/{test.length}] {question.value}",
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

                    await bot.send_message(chat_id=user_id, 
                                           text=test.get_resolts(), 
                                           reply_markup=DefoltButton.user_home_menu)


    