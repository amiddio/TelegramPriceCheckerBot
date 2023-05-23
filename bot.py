import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import load_config, Config
from keyboards.set_menu import set_main_menu
from handlers import user_handlers
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from lexicon.lexicon import LEXICON_GENERAL_RU
from scheduler.scheduler import set_scheduled_jobs


async def main() -> None:

    # Load config data
    config: Config = load_config()

    # Init scheduler
    scheduler = AsyncIOScheduler()

    # Init bot and dispatcher
    bot: Bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
    dp: Dispatcher = Dispatcher()

    # Add menu button
    await set_main_menu(bot)

    # Register routers in dispatcher
    dp.include_router(user_handlers.router)

    # Ignored some old updates and run polling
    await bot.delete_webhook(drop_pending_updates=True)

    # Add job to scheduler and start it
    set_scheduled_jobs(scheduler, bot, config.interval_parse)
    scheduler.start()

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print(LEXICON_GENERAL_RU["Bot stopped"])



