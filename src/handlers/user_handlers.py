import random

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..lexicon.lexicon import LEXICON
from ..services.contacting_the_exchange import exchange_rate_random
from ..fsm.fsm import storage, default_state, user_answer, FSMexchangeform, fsm_exchange_form_state
from ..filters.filters import InStatesFilter, CheckingLetterCode

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


@router.message(Command(commands='exchange'))
async def process_exchange_command(message: Message, state: FSMContext):
    """ Этот хендлер будет срабатывать на команду '/exchange'
        менять машинное состояния с 'default_state' на 'fill_first_question'
        и будет задавать первый вопрос. """
    await message.answer(text='Введите сумму желаемую к обмену\n\n')
    # Ожидаем ответа на вопрос в корректном формате
    await state.set_state(FSMexchangeform.fill_first_question)


@router.message(Command(commands='cancel'), InStatesFilter(fsm_exchange_form_state))
async def process_cancel_command_state_exchange(message: Message, state: FSMContext):
    """ Этот хендлер будет срабатывать на команду '/cancel'
        когда бот находиться внутри 'FSMexchangeform'. """
    await message.answer(text=
                         "Вы вышли из обменника!\n\n Для возврата к обмену введите команду"
                         " '/exchange'. ")
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@router.message(StateFilter(FSMexchangeform.fill_first_question), F.text.isdigit())
async def process_first_answer_sent(message: Message, state: FSMContext):
    """ Этот хендлер будет срабатывать если данные будут корректно введены.
        Менять машинное состояние с 'fill_first_question' на 'second_first_question'
        Задает второй вопрос"""
    await state.update_data(fq=message.text)
    await message.answer(text='Введите вашу валюту')
    await state.set_state(FSMexchangeform.fill_second_question)


@router.message(StateFilter(FSMexchangeform.fill_second_question), CheckingLetterCode())
async def process_second_answer_sent(message: Message, state: FSMContext):
    """ Правильный ответ на вопрос 2"""
    await state.update_data(sq=message.text)
    await message.answer(text='Введите вторую валюту')
    await state.set_state(FSMexchangeform.fill_third_question)






# @router.message()
# async def process_exchange_commande(message: Message):
#     er = await exenge_rate_random()
#     random_keys = random.choice(list(er.keys()))
#     await message.answer(f'1 EUR = {er[random_keys]} {random_keys}')
