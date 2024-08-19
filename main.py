from src import *
from src.bot import bot, dp
from src.config import main as logger, commands
import asyncio


async def run():
    init_log()
    await init_db()
    dp.include_routers(*routers)
    logger.info(f"START bot polling")
    await bot.set_my_commands(commands)
    await dp.start_polling(bot, polling_timeout=5)
    logger.info(f"END bot polling")


if __name__ == "__main__":
    asyncio.run(run())
