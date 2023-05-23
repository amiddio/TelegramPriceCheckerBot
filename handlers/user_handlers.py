from aiogram import Router
from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message, CallbackQuery
from config_data.chat import save_chat_id
from lexicon.lexicon import LEXICON_GENERAL_RU
from models.link_orm import LinkOrm
from parser.runner import run, get_message

# Init router
router: Router = Router()


# Catch the command '/start'
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_GENERAL_RU['/start'])
    if message.chat.id:
        save_chat_id(str(message.chat.id))


# Catch the command '/help'
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_GENERAL_RU['/help'])


# Catch the command '/parse'
@router.message(Command(commands='parse'))
async def process_parse_command(message: Message):
    links: list[LinkOrm] = run()
    if links:
        for link in links:
            await message.answer(text=get_message(link))
    else:
        await message.answer(text=LEXICON_GENERAL_RU["products not changed"])


@router.message()
async def echo_sent(message: Message):
    await message.answer(text=LEXICON_GENERAL_RU["echo message"])
