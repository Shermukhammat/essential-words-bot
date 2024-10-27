import sqlite3
from .table import creat_tables
from .users import UsersDb, Status, User
from asyncio import Semaphore
from .params import ParamsDB


class DataBase(UsersDb, ParamsDB):
    def __init__(self, path : str, config_file : str = 'config.yaml') -> None:
        creat_tables(path) 
        self.write_semapore = Semaphore()
        
        UsersDb.__init__(self, path, write_semapore = self.write_semapore)
        ParamsDB.__init__(self, config_file)
