import sqlite3
from .clock import now
from .cache import Cache
from asyncio import Semaphore

class Status:
    active = 1
    blocked = 2

class User:
    def __init__(self, 
                 id : int = None, 
                 name : str = None, 
                 lang : str = 'uz',
                 status : int = Status.active, 
                 registred : str = None) -> None:
        self.id = id
        self.name = name
        self.lang = lang
        self.status = status
        self.registred = registred  
 


class UsersDb:
    def __init__(self, db_path : str, write_semapore : Semaphore, cache_leng : int = 100) -> None:
        self.path = db_path 
        self.users_cache : Cache = Cache(max_len = cache_leng)
        self.write_semapore = write_semapore
    
    def is_user(self, id : int) -> bool:
        if self.users_cache.data.get(id):
            return True
        
        user = get_user_from_db(self.path, id)
        if user:
            return True
        return False

    async def register_user(self, id : int, name : str = "", lang : str = 'uz') -> bool:
        time = now()
        status = Status.active

        async with self.write_semapore:
            try:
                con = sqlite3.connect(self.path)
                cursor = con.cursor()
                cursor.execute("INSERT INTO users (id, registered, status, name, lang) VALUES(?, ?, ?, ?, ?);", (id, time, status, name, lang))

                con.commit()
                con.close()

                await self.users_cache.set(id, User(id = id, name = name, lang = lang, status=status))
                return True
        
            except Exception as e:
                print(e)
                return False
            
    
    async def get_user(self, id) -> User:
        user = await self.users_cache.get(id)
        if user:
            return user
        
        user = get_user_from_db(self.path, id)
        if user:
            await self.users_cache.set(user.id, user)
            return user 
        
    
    async def remove_user(self, id):
        await self.users_cache.delete(id)

        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        
        cursor.execute(f"DELETE FROM users WHERE id = ?;", (id,))
        
        con.commit()
        con.close()

    async def update_user_status(self, id : int, status : int) -> bool:
        """_summary_

        Args:
            id (int): _description_
            status (int): 0 is blocked, 1 is not blocked

        Returns:
            bool: _description_
        """
        user : User = await self.users_cache.get(id)
        if user:
            user.status = status
            await self.users_cache.delete(id)
            await self.users_cache.set(id, user)
        
        async with self.write_semapore:
            return updat_user_db_status(self.path, status, id)
    
    async def update_user_lang(self, id : int, lang : str):
        user : User = await self.users_cache.get(id)
        if user:
            user.lang = lang
            await self.users_cache.delete(id)
            await self.users_cache.set(id, user)

        async with self.write_semapore:   
            return update_user_db_lang(self.path, lang, id)
    

    def get_users(self) -> list[dict]:
        return get_users_from_db(self.path)
    


def update_user_db_lang(path : str, lang : str, id : int) -> bool:
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        
        cursor.execute(f"UPDATE users SET lang = ? WHERE id = ?;", (lang, id))
        
        con.commit()
        con.close()
        return True
    
    except Exception as e:
        print(e)
        return False


def updat_user_db_status(path : str, status : int, id : int) -> bool:
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        
        cursor.execute(f"UPDATE users SET status = {status} WHERE id = {id};")
        
        con.commit()
        con.close()
        return True
    
    except Exception as e:
        print("updat_user_db_status: ", e)
        return False
    
def get_user_from_db(db_path : str, id : int) -> User:
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    
    for row in cursor.execute(f"SELECT registered, status, name, lang FROM users WHERE id = {id};"):
        con.close()
        # return {'registered' : row[0], 'status' : row[1], 'name' : row[2], 'lang' : row[3]}
        return User(registred = row[0], status = row[1], name = row[2], lang=row[3], id = id)
    
    con.close()


def get_users_from_db(db_path : str) -> list[dict]:
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    users = []
    for row in cursor.execute(f"SELECT registered, status, name, lang, id FROM users;"):
        users.append({'registered' : row[0], 'status' : row[1], 'name' : row[2], 'lang' : row[3], 'id' : row[4]})
    
    con.close()
    return users
    

if __name__ == '__main__':
    db = UsersDb('test.db')

