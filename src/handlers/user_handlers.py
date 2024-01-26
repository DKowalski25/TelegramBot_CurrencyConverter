from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from sqlalchemy.orm import sessionmaker

from src.lexicon import LEXICON
from src.database import register_new_user, get_exchange_history, format_exchange_history

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, session_maker: sessionmaker):
    """
    This handler will be triggered by the command '/start'
    Send a welcome message to the user.
    """

    user_id = message.from_user.id
    user_name = message.from_user.username

    await register_new_user(user_id, user_name, session_maker=session_maker)
    await message.answer(text=LEXICON[message.text])


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    """
    This handler will be triggered by the command '/help'
    and send a message to the user with a list of available commands in the bot.
    """

    await message.answer(text=LEXICON[message.text])


@router.message(Command(commands='history'))
async def process_history_command(message: Message, session_maker: sessionmaker):
    """
    This handler will be triggered by the command '/history'.
    And send a message to the user with a list
    of the exchange history.
    """

    user_id = message.from_user.id
    history = await get_exchange_history(user_id, session_maker)
    formatted_history = await format_exchange_history(history)
    await message.answer(formatted_history)





