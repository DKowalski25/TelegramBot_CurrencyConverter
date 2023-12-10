import json

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from ..lexicon.lexicon import LEXICON
from ..services.contacting_the_exchange import exchange_rate
from ..services.user_db_check import check_user_in_db
from ..fsm.fsm import FSMexchangeform, fsm_exchange_form_state
from ..filters.filters import InStatesFilter, CheckingLetterCode
from ..keyboards.exchange_keyboard import create_exchange_keyboard
from ..database.redis import user_answer, storage, r

router = Router()


@router.message(Command(commands='exchange'))
async def process_exchange_command(message: Message, state: FSMContext):
    """ Этот хендлер будет срабатывать на команду '/exchange'
        менять машинное состояния с 'default_state' на 'fill_first_question'
        и будет задавать первый вопрос. """
    user_id = message.from_user.id
    if user_id not in user_answer:
        user_answer[user_id] = {}
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

    user_id = message.from_user.id
    user_data = await state.get_data()

    # Получаем текущий номер пользователя и увеличиваем его на 1
    current_number = len(user_answer[user_id]) + 1

    # Сохраняем данные пользователя с использованием текущего номера
    user_answer[user_id][current_number] = user_data

    amount = int(user_data['fq'])
    cur1 = user_data['sq']
    cur2 = user_data['tq']

    ans = await (exchange_rate(amount, cur1, cur2))

    await message.answer(text=f'{amount} {cur1} = {ans} {cur2}')
    await state.update_data(summ=ans)

    user_answer[user_id][current_number] = await state.get_data()

    await message.answer(text='Хотите сделать еще один обмен?',
                         reply_markup=create_exchange_keyboard())
    await state.set_state(FSMexchangeform.fill_fourth_question)


@router.callback_query(StateFilter(FSMexchangeform.fill_fourth_question),
                       F.data.in_(['exchange_more']))
async def process_yes_button_sent(callback: CallbackQuery, state: FSMContext):
    """ Этот хендлер срабатывает нажатие кнопки YES. """
    await callback.message.answer(text='\n\nВведите сумму желаемую к обмену\n\n')

    json_user_answer = json.dumps(user_answer)

    await r.set(callback.from_user.id, json_user_answer)
    await state.clear()
    await state.set_state(FSMexchangeform.fill_first_question)


@router.callback_query(StateFilter(FSMexchangeform.fill_fourth_question),
                       F.data.in_(['no_exchange']))
async def process_no_button_sent(callback: CallbackQuery, state: FSMContext):
    """ Этот хендлер срабатывает на нажатие кнопки NO. """
    await callback.message.answer(text='Приходи еще')
    json_user_answer = json.dumps(user_answer)
    await r.set(callback.from_user.id, json_user_answer)
    await state.clear()
