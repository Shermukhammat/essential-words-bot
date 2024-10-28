from data import BookData





book_db = BookData('data/book1.yaml')

unit1 = book_db.units[1]
for p, word in unit1.words.items():
    print(p, word.value, word.translation)