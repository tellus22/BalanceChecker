import asyncio

from Handlers import dp
from aiogram import executor

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=True)
