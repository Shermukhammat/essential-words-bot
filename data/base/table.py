import sqlite3


def creat_tables(path : str):
    con = sqlite3.connect(path)
    cursor = con.cursor()
    
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name, registered, status INTEGER, lang); """)
    cursor.execute(""" CREATE TABLE IF NOT EXISTS admins(id INTEGER PRIMARY KEY, name, registered, type INTEGER, lang, notification INTEGER); """)
    
    con.commit()
    con.close()
    
    