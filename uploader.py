from data import DataBase
from aiogram import Bot, types, Dispatcher
from aiogram.bot.api import TelegramAPIServer
import asyncio
import pandas as pd



db = DataBase('data/data.db')




# data = pd.read_csv('row_data3.csv')
# data['sound1_data_id'] = "none"
# data['image_data_id'] = "none"
# data.to_csv('row_data4.csv', index_label=False)


data = pd.read_csv('row_data4.csv')


async def main():
    server = TelegramAPIServer.from_base('http://127.0.0.1:1111')
    bot = Bot(token = db.TOKEN, server=server)

    for index in data.index:
        if data.loc[index, 'sound1_data_id'] == "none":
            book = data.loc[index, 'book']
            sound = data.loc[index, 'sound1']
            unit = data.loc[index, 'unit']

            print(f"Book: {book} unit: {unit} uploading: {sound}                   ", end='\r')

            message_data = await bot.send_audio(chat_id=db.DATA_CHANEL, 
                                                audio=open(f"data/media/book{book}/{sound}", 'rb'))
            
            data.loc[index, 'sound1_data_id'] = message_data.message_id
            data.to_csv('row_data4.csv', index_label=False)

            await asyncio.sleep(3)
        
        # if data.loc[index, 'image_data_id'] == "none":
        #     book = data.loc[index, 'book']
        #     image = data.loc[index, 'image']
        #     unit = data.loc[index, 'unit']

        #     print(f"Book: {book} unit: {unit} uploading: {image}                            ", end='\r')

        #     message_data = await bot.send_photo(chat_id=db.DATA_CHANEL, 
        #                                         photo=open(f"data/media/book{book}/{image}", 'rb'))
            
        #     data.loc[index, 'image_data_id'] = message_data.message_id
        #     data.to_csv('row_data4.csv', index_label=False)
            
        #     await asyncio.sleep(3)

    sesion = await bot.get_session()
    if sesion:
        await sesion.close()
    print("All data has been uploaded", " "*30)


asyncio.run(main())
