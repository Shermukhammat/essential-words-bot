from loader import dp, db, bot
from aiogram import types
from uuid import uuid4


# {"message_id": 12, "sender_chat": {"id": -1002359587138, "title": "Essential Data", "username": "audiotd", "type": "channel"}, 
#  "chat": {"id": -1002359587138, "title": "Essential Data", "username": "audiotd", "type": "channel"}, 
#  "date": 1730276435, 
#  "audio": {"duration": 0, 
#            "file_name": 
#            "angry_1392933884419.mp3", 
#            "mime_type": "audio/mpeg", 
#            "file_id": "CQACAgIAAyEGAASMpHFCAAMMZyJOw0BsoehSw3ZQIoAbdemve-IAAglsAAKJvRlJZOj_tMSL9lE2BA", 
#            "file_unique_id": "AgADCWwAAom9GUk", "file_size": 22601}, 
#  "caption": "blah"}

@dp.inline_handler()
async def inline_audio(query: types.InlineQuery):
    audio_result = types.InlineQueryResultAudio(
        id=uuid4().hex,
        title="Blah",
        audio_url="https://t.me/audiotd/12",
        
        caption="Here's your requested audio!",
    )
    # Answer the inline query
    await bot.answer_inline_query(query.id, results=[audio_result], cache_time=1)


