from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config_data.chat import get_chat_id
from lexicon.lexicon import LEXICON_GENERAL_RU
from logger.logger import log
from models.link_orm import LinkOrm
from parser.runner import run, get_message


def set_scheduled_jobs(scheduler: AsyncIOScheduler, bot: Bot, interval: int) -> None:
    """
    Добавление задачи планировщику

    :param scheduler: AsyncIOScheduler
    :param bot: Bot
    :param interval: interval
    :return: None
    """

    sec = interval * 60 * 60
    scheduler.add_job(_run_parser, "interval", seconds=sec, args=(bot,))


async def _run_parser(bot: Bot) -> None:
    """
    Метод который будет запускаться через определенные интервалы.
    В случае изменении статсу/цены продукта в этом методе отправляется сообщение для боту.

    :param bot: Bot
    :return: None
    """

    try:
        chat_id = get_chat_id()
        if chat_id:
            links: list[LinkOrm] = run()
            if links:
                for link in links:
                    text = get_message(link)
                    await bot.send_message(text=text, chat_id=chat_id)
    except (AttributeError, Exception) as e:
        log().error(str(e))

