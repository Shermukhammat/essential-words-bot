import sqlite3
from .clock import now
from asyncio import Semaphore
from .cache import Cache

class AdminType:
    owner = 1
    usual = 2
    

class Admin:
    def __init__(self, 
                 id : int = None,
                 registered : str = None,
                 admin_type : int = AdminType.usual,
                 name : str = "none",
                 lang : str = 'uz',
                 notification : int = 0) -> None:
        self.id = id
        self.registered = registered
        self.admin_type = admin_type
        self.name = name
        self.lang = lang
        self.notification = notification


class AdminsDb:
    def __init__(self, db_path : str, write_semapore : Semaphore, cache_leng : int = 100) -> None:
        self.path = db_path 
        self.write_semapore = write_semapore
        self.admins_cache = Cache(max_len=cache_leng)
    
    async def is_admin(self, id : int) -> bool:
        if await self.admins_cache.get(id):
            return True
        
        admin = get_admin_from_db(self.path, id)
        if admin:
            await self.admins_cache.set(admin.id, admin)
            return True
        return False

    async def register_admin(self, id : int, name : str, lang : str = 'uz', admin_type : int = AdminType.usual, notification : bool = 0) -> bool:
        time = now()
        async with self.write_semapore:
            try:
                con = sqlite3.connect(self.path)
                cursor = con.cursor()
                cursor.execute("INSERT INTO admins (id, registered, type, name, lang, notification) VALUES(?, ?, ?, ?, ?, ?);", (id, time, admin_type, name, lang, notification))

                con.commit()
                con.close()

                await self.admins_cache.set(id, Admin(id=id, registered=time, admin_type=admin_type, name=name, lang=lang, notification=0))
                return True
        
            except Exception as e:
                print("register_admin", e)
                return False
        
    
    async def get_admin(self, id) -> Admin:
        admin = await self.admins_cache.get(id)
        if admin:
            return admin
        
        admin = get_admin_from_db(self.path, id)
        if admin:
            await self.admins_cache.set(admin.id, admin)
            return admin 
        
    
    async def get_admins(self) -> list[Admin]:
        return get_admins_from_db(self.path)

        
    
    async def remove_admin(self, id):
        await self.admins_cache.delete(id)
        
        async with self.write_semapore:
            con = sqlite3.connect(self.path)
            cursor = con.cursor()
        
            cursor.execute(f"DELETE FROM admins WHERE id = ?;", (id,))
        
            con.commit()
            con.close()

    async def update_admin_lang(self, id : int, lang : str) -> bool:
        admin : Admin = await self.admins_cache.get(id)
        if admin:
            await self.admins_cache.delete(id)
            admin.lang = lang
            await self.admins_cache.set(id, admin)
        
        async with self.write_semapore:
            return update_admin_db_lang(self.path, lang, id)
    
    async def update_admin_notification(self, id : int, notification : int) -> bool:
        admin : Admin = await self.admins_cache.get(id)
        if admin:
            await self.admins_cache.delete(id)
            admin.notification = notification
            await self.admins_cache.set(id, admin)
        
        async with self.write_semapore:
            return update_admin_db_notification(self.path, notification, id)


def update_admin_db_notification(path : str, notification : int, id : int) -> bool:
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        
        cursor.execute(f"UPDATE admins SET notification = ? WHERE id = ?;", (notification, id))
        
        con.commit()
        con.close()
        return True
    
    except:
        return False


def update_admin_db_lang(path : str, lang : str, id : int) -> bool:
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        
        cursor.execute(f"UPDATE admins SET lang = ? WHERE id = ?;", (lang, id))
        
        con.commit()
        con.close()
        return True
    
    except Exception as e:
        print("update_admin_db_lang", e)
        return False
    

    
def get_admin_from_db(db_path : str, id : int) -> Admin:
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    
    for row in cursor.execute(f"SELECT name, registered, type, lang, notification FROM admins WHERE id = ?;", (id,)):
        con.close()
        # return {'registered' : row[1], 'type' : row[2], 'name' : row[0], 'lang' : row[3], 'notification' : row[4]}
        return Admin(id=id, registered = row[1], admin_type = row[2], name=row[0], lang=row[3], notification=row[4])
    con.close()
    

def get_admins_from_db(db_path : str) -> list[Admin]:
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    data = []
    for row in cursor.execute(f"SELECT name, registered, type, lang, notification, id FROM admins;"):
        # {'registered' : row[1], 'type' : row[2], 'name' : row[0], 'lang' : row[3], 'notification' : row[4], 'id' : row[5]}
        data.append(Admin(id=row[5], registered = row[1], admin_type = row[2], name=row[0], lang=row[3], notification=row[4]))
    
    con.close()
    return data


if __name__ == '__main__':
    db = AdminsDb('test.db')
    # db.register_admin(2, 'sher2')
    # db.remove_admin(2)
    # db.get_admin(2)
    
    # db.update_user_status(1, Status.blocked)
    print(db.admins_cache)