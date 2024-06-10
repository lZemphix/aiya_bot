import asyncio, os
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import stated_commands

dotenv_path = Path('data/.env')
load_dotenv(dotenv_path=dotenv_path)

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()



async def main():
    dp.include_routers(stated_commands.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    


if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: print("Bot was stopped")
