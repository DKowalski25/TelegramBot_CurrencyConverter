import random

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from ..lexicon.lexicon import LEXICON
from ..services.contacting_the_exchange import exenge_rate_random

router = Router()

"""Этот хендлер будет срабатывать на команду '/start'"""
"""Отправлять пользователю приветственное сообщение"""


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON[message.text])


"""Этот хэндлер будет срабатывать на команду '/help'"""
"""и отправлять пользователю сообщение со списком доступных команд в боте"""


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON[message.text])


"""Этот хендлер будет срабатывать на любое сообщение"""
"""и выдавать заранее задую валютную пару"""


@router.message()
async def process_currency_change(message: Message):
    er = await exenge_rate_random()
    random_keys = random.choice(list(er.keys()))
    await message.answer(f'1 EUR = {er[random_keys]} {random_keys}')
