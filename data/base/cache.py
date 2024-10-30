from asyncio import Semaphore


class Cache:
    def __init__(self, max_len : int = 10) -> None:
        self.data = {}
        self.max_len = max_len
        self.lock = Semaphore(1)


    async def set(self, key, value):
        async with self.lock:
            self.data[key] = value
            
            if len(self.data) > self.max_len:
                self.data.popitem()

            
    async def get(self, key):
        return self.data.get(key)
    

    async def delete(self, key):
        async with self.lock:
            if self.data.get(key):
                del self.data[key]
