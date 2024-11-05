from data import BookData, DataBase
import asyncio




books = {n : BookData(f'data/book{n}.yaml') for n in range(1, 7)}

# unit1 = book_db.units[1]
# for p, word in unit1.words.items():
#     print(p, word.value, word.translation)

db = DataBase('data/data.db')


async def main():
    for book in books.values():
        for unit in book.units.values():
            await db.set_unit(unit)
    # if unti:
    #     await db.set_unit(unti)
    # await db.get_unit(1, 1)
    # unti = await db.get_unit(1, 1)
    # print(unti.get_words_text())

asyncio.run(main())