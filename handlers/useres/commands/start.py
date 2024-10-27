from loader import db, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from utilites.states.useres import UserRegistrState


@dp.message_handler(commands = 'start')
async def start_registr_handler(update : types.Message, state : FSMContext):
    await state.set_state(UserRegistrState.get_lang)
    await update.answer("Iltimos tilni tanlag")
    # await db.register_user(update.from_user.id, name=update.from_user.first_name)