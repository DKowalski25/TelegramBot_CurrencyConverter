import random

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..lexicon.lexicon import LEXICON
from ..services.contacting_the_exchange import exchange_rate
from ..fsm.fsm import default_state, user_answer, FSMexchangeform, fsm_exchange_form_state
from ..filters.filters import InStatesFilter, CheckingLetterCode

router = Router()


@router.message(Command(commands='exchange'))
async def process_exchange_command(message: Message, state: FSMContext):
    """ Этот хендлер будет срабатывать на команду '/exchange'
        менять машинное состояния с 'default_state' на 'fill_first_question'
        и будет задавать первый вопрос. """
    await message.answer(text='\n\nВведите сумму желаемую к обмену\n\n')
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


@router.message(StateFilter(FSMexchangeform.fill_first_question))
async def warring_not_digit(message: Message):
    """ Этот хендлер будет срабатывать если ввели что-то отличающиеся от цифр. """
    await message.answer(
        text="Введено не корректное значение\n\nПопробуйте ещё раз")


@router.message(StateFilter(FSMexchangeform.fill_second_question), CheckingLetterCode())
async def process_second_answer_sent(message: Message, state: FSMContext):
    """ Правильный ответ на вопрос 2"""
    await state.update_data(sq=message.text)
    await message.answer(text='Введите вторую валюту')
    await state.set_state(FSMexchangeform.fill_third_question)


@router.message(StateFilter(FSMexchangeform.fill_second_question))
async def warring_not_currency_code(message: Message):
    """ Этот хендлер будет срабатывать если введенная информация юзером
     не совпадает с форматом кода валюты. """
    await message.answer(
        text="Введено не корректное значение\n\nПопробуйте ещё раз")


@router.message(StateFilter(FSMexchangeform.fill_third_question), F.text.isdigit)
async def process_third_answer_sent(message: Message, state: FSMContext):
    """ Правильный ответ на вопрос 3"""
    await state.update_data(tq=message.text)
    user_answer[message.from_user.id] = await state.get_data()
    # await message.answer(text=f"fq = {user_answer[message.from_user.id]['fq']}\n"
    #                           f"sq = {user_answer[message.from_user.id]['sq']}\n"
    #                           f"tq = {user_answer[message.from_user.id]['tq']}\n")
    amount = int(user_answer[message.from_user.id]['fq'])
    cur1 = user_answer[message.from_user.id]['sq']
    cur2 = user_answer[message.from_user.id]['tq']
    ans = await (exchange_rate(amount, cur1, cur2))
    await message.answer(text=f'{ans}')
    # Завершаем машину состояний
    await state.clear()
