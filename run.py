import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv

from app.handlers import router as main_router

load_dotenv()

storage = RedisStorage.from_url(f"redis://@localhost:6379/0")
BOT_TOKEN: str = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)
dp.include_router(main_router)


async def main() -> None:
    await asyncio.gather(
        dp.start_polling(bot, skip_updates=True),
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped.")
