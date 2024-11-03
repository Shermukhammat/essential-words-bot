from aiogram import Bot, types, Dispatcher
from aiogram.bot.api import TelegramAPIServer
import asyncio
import pandas as pd
from data import DataBase
from tokens import SCRAPER_BOT_TOKEN






# data = pd.read_csv('screenshots.csv')

# data['wordlist_photo1_data_id'] = "none"
# data['wordlist_photo2_data_id'] = "none"

# data['exercise_photo1_data_id'] = "none"
# data['exercise_photo2_data_id'] = "none"

# data['story_photo_data_id'] = "none"
# data['story_exercise_photo_data_id'] = "none"

# data.to_csv('screenshots2.csv', index_label=False)

db = DataBase('data/data.db')
data = pd.read_csv('screenshots2.csv')

columns = {
    'wordlist_photo1':'wordlist_photo1_data_id',
    'wordlist_photo2':'wordlist_photo2_data_id',
    'exercise_photo1':'exercise_photo1_data_id',
    'exercise_photo2':'exercise_photo2_data_id',
    'story_photo':'story_photo_data_id',
    'story_exercise_photo':'story_exercise_photo_data_id'
}

async def main():
    bot = Bot(SCRAPER_BOT_TOKEN)

    for index in data.index:
        for column, column_data_id in columns.items():
            await upload(data=data, 
                         index=index,
                         colum_data_id=column_data_id,
                         column=column,
                         bot=bot)

     

              
    sesion = await bot.get_session()
    if sesion:
        await sesion.close()
    
    print("All photos uploaded", " "*30)


async def upload(data : pd.DataFrame = None,
                 index : int = None,
                 colum_data_id : str = None,
                 column : str = None,
                 bot : Bot = None):
    
    if data.loc[index, colum_data_id] == 'none':
        page = data.loc[index, column]
        book = data.loc[index, 'book']
        unit = data.loc[index, 'unit']

        print(f"uploading book: {book} unit: {unit}  {column}                         ", end='\r')

        message_data = await bot.send_photo(chat_id=db.DATA_CHANEL,
                                 photo=open(f"data/books/imgs/book{book}/page{page}.png", 'rb'))
        
        data.loc[index, colum_data_id] = message_data.message_id
        data.to_csv('screenshots2.csv', index_label=False)

        await asyncio.sleep(3)




asyncio.run(main())