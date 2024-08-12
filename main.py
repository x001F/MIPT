from src import get_logger
from src import routers
from src import dp, bot
from src import init_db
# from src import set_commands
import asyncio

logger = get_logger("main")


async def run():
    await init_db()
    dp.include_routers(*routers)
    logger.info(f"START bot polling")
    # await set_commands()
    await dp.start_polling(bot, polling_timeout=5)
    logger.info(f"END bot polling")


if __name__ == "__main__":
    asyncio.run(run())
