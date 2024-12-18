from asyncio import Semaphore
from aiogram.dispatcher import FSMContext

async def get_semaphore(state : FSMContext) -> Semaphore:
    state_data = await state.get_data()
    if state_data.get('semaphore'):
        return state_data['semaphore']
    
    