from loader import db, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from utilites.states.useres import UserState
from utilites.buttons import DefoltButton
import re



@dp.message_handler(state=UserState.unit_menu)
async def unit_menu_handler(update : types.Message, state : FSMContext):
    state_data = await state.get_data()

    