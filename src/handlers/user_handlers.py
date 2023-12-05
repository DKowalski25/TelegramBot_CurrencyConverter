from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from ..lexicon.lexicon import LEXICON

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    """ Этот хендлер будет срабатывать на команду '/start'
        Отправлять пользователю приветственное сообщение. """
    await message.answer(text=LEXICON[message.text])


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    """ Этот хэндлер будет срабатывать на команду '/help'
        и отправлять пользователю сообщение со списком доступных команд в боте. """
    await message.answer(text=LEXICON[message.text])
