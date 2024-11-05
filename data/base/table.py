import sqlite3


def creat_tables(path : str):
    con = sqlite3.connect(path)
    cursor = con.cursor()
    
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name, registered, status INTEGER, lang); """)
    cursor.execute(""" CREATE TABLE IF NOT EXISTS admins(id INTEGER PRIMARY KEY, name, registered, type INTEGER, lang, notification INTEGER); """)
    
    cursor.execute(""" CREATE TABLE IF NOT EXISTS units(id INTEGER PRIMARY KEY, data);""")
    # cursor.execute(""" CREATE TABLE IF NOT EXISTS photos(book INTEGER, unit INTEGER, photo INTEGER);""")
    # cursor.execute(""" CREATE TABLE IF NOT EXISTS exercise(book INTEGER, unit INTEGER, photo INTEGER);""")
    # cursor.execute(""" CREATE TABLE IF NOT EXISTS reading(book INTEGER, unit INTEGER, photo1 INTEGER, photo2 INTEGER, audio INTEGER);""")

    con.commit()
    con.close()
    
    