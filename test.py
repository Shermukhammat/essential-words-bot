from data import BookData, DataBase
import asyncio




# book_db = BookData('data/book1.yaml')

# unit1 = book_db.units[1]
# for p, word in unit1.words.items():
#     print(p, word.value, word.translation)

db = DataBase('test.db')


async def main():
    # unti = book_db.units.get(1)
    # if unti:
    #     await db.set_unit(unti)
    await db.get_unit(1, 1)
    unti = await db.get_unit(1, 1)
    print(unti.get_words_text())

asyncio.run(main())