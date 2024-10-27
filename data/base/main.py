import sqlite3
from .table import creat_tables
from .users import UsersDb, Status, User
from asyncio import Semaphore
from .params import ParamsDB
from .admins import Admin, AdminsDb, AdminType
from aiogram.types import User

class DataBase(UsersDb, ParamsDB, AdminsDb):
    def __init__(self, path : str, config_file : str = 'config.yaml') -> None:
        creat_tables(path) 
        self.write_semapore = Semaphore()
        self.bot : User = None

        UsersDb.__init__(self, path, write_semapore = self.write_semapore, cache_leng=100)
        ParamsDB.__init__(self, config_file)
        AdminsDb.__init__(self, path, write_semapore = self.write_semapore, cache_leng=100)

    
    def init_bot_info(self, info : User):
        self.bot = info
