from discord.ext import tasks
import asyncio


class Cache:
    def __init__(self):
        self.cache_update_loop.start()
        print('__init__')

    @tasks.loop(seconds=1)
    async def cache_update_loop(self):
        print(1)

    @cache_update_loop.before_loop
    async def before_cache_update_loop(self):
        print('before loop')


async def main():
    cache = Cache()
    await asyncio.sleep(5)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
