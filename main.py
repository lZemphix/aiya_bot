import asyncio

from aiogram import Bot, Dispatcher
from data.config import TOKEN
from handlers import stated_commands


bot = Bot(TOKEN)
dp = Dispatcher()



async def main():
    dp.include_routers(stated_commands.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
