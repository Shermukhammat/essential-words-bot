# from data import BookData, DataBase
# from utilites import get_questions
# import asyncio
# from datetime import datetime




# # book_db = BookData('data/book1.yaml')

# # unit1 = book_db.units[1]
# # for p, word in unit1.words.items():
# #     print(p, word.value, word.translation)

# db = DataBase('test.db')


# async def main():
#     # unti = book_db.units.get(1)
#     # if unti:
#     #     await db.set_unit(unti)
#     start = datetime.now()
#     # await db.get_unit(1, 1)
#     unti = await db.get_unit(1, 1)
    
    
#     questions = get_questions([unti], uzen=False, mix=True, definition=True)
#     for question in questions:
#         print(question.value, "->", question.answer, question.options)

#     print(datetime.now() - start)

# asyncio.run(main())

def seconds_to_human_readable(seconds):
    hours, seconds = divmod(seconds, 3600)  # 3600 seconds in an hour
    minutes, seconds = divmod(seconds, 60)  # 60 seconds in a minute

    # Create a human-readable string
    parts = []
    if hours > 0:
        parts.append(f"{hours} soat")
    if minutes > 0:
        parts.append(f"{minutes} minut")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} sec")

    return ', '.join(parts)

# Example usage
print(seconds_to_human_readable(7345))
