import json

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from ..lexicon.lexicon import LEXICON
from ..database.redis import user_answer, r

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


@router.message(Command(commands='history'))
async def process_history_command(message: Message):
    """ Этот хендлер будет срабатывать на команду '/history'.
        И отправлять пользователю сообщение со списком
        истории обмена"""
    data = await r.get(message.from_user.id)
    retrieved_dict = json.loads(data)
    await message.answer(text=f'{retrieved_dict}')
