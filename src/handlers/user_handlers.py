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
    data = await r.get(str(message.from_user.id))
    retrieved_dict = json.loads(data)
    user_id = message.from_user.id
    await message.answer(text=f'{retrieved_dict}')

    # def normalization_answer(ua: dict):
    #     result_str_list = []
    #     for outer_key, inner_dict in ua.items():
    #         for inner_key, inner_values in inner_dict.items():
    #             fq = inner_values['fq']
    #             sq = inner_values['sq']
    #             tq = inner_values['tq']
    #             summ = inner_values['summ']
    #
    #             result_str = f"{inner_key}: {fq} {sq} to {tq} = {summ}"
    #             result_str_list.append(result_str)
    #     return '\n'.join(result_str_list)
    # await message.answer(text=f'{normalization_answer(data)}')



    #
    # async def print_inner_dict(inner_dict):
    #     """ Функция для вывода ключей и значений внутреннего словаря. """
    #     for key, value in inner_dict.items():
    #         await message.answer(text=f'   {key}: {value}')
    #
    # await print_inner_dict(desired_inner_dict)
