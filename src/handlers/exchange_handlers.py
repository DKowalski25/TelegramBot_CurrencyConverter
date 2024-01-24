from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from sqlalchemy.orm import sessionmaker

from src.database import add_exchange_history
from src.services import exchange_rate
from src.utils.fsm.fsm import FSMexchangeform, fsm_exchange_form_state
from src.utils.filters.filters import InStatesFilter, CheckingLetterCode
from src.keyboards import create_exchange_keyboard

router = Router()


@router.message(Command(commands='exchange'))
async def process_exchange_command(message: Message, state: FSMContext):
    """
    This handler will be triggered by the command '/exchange'
    change FMS from 'default_state' to 'fill_first_question'
    and he will ask the first question.
    """

    await message.answer(text='\n\nВведите сумму желаемую к обмену\n\n')
    await state.set_state(FSMexchangeform.fill_first_question)


@router.message(Command(commands='cancel'), InStatesFilter(fsm_exchange_form_state))
async def process_cancel_command_state_exchange(message: Message, state: FSMContext):
    """
    This handler will be triggered by the command '/cancel'
    when the bot is inside the 'FSMexchangeform'.
    """

    await message.answer(text=
                         "Вы вышли из обменника!\n\n Для возврата к обмену введите команду"
                         " '/exchange'. ")
    await state.clear()


@router.message(StateFilter(FSMexchangeform.fill_first_question), F.text.isdigit())
async def process_first_answer_sent(message: Message, state: FSMContext):
    """
    This handler will be triggered if the data is entered correctly.
    Change the machine state from 'fill_first_question' to 'fill_second_question'
    Asks the second question.
    """

    await state.update_data(fq=message.text)
    await message.answer(text='Введите вашу валюту')
    await state.set_state(FSMexchangeform.fill_second_question)


@router.message(StateFilter(FSMexchangeform.fill_first_question))
async def warring_not_digit(message: Message):
    """This handler will be triggered if you entered something different from the numbers."""
    await message.answer(
        text="Введено не корректное значение\n\nПопробуйте ещё раз")


@router.message(StateFilter(FSMexchangeform.fill_second_question), CheckingLetterCode())
async def process_second_answer_sent(message: Message, state: FSMContext):
    """
    This handler will be triggered if the data is entered correctly.
    Change the machine state from 'fill_second_question' to 'fill_third_question'
    Asks the third question.
    """

    await state.update_data(sq=message.text)
    await message.answer(text='Введите вторую валюту')
    await state.set_state(FSMexchangeform.fill_third_question)


@router.message(StateFilter(FSMexchangeform.fill_second_question))
async def warring_not_currency_code(message: Message):
    """
    This handler will be triggered if the information entered by the user
    does not match the format of the currency code.
    """

    await message.answer(
        text="Введено не корректное значение\n\nПопробуйте ещё раз")


@router.message(StateFilter(FSMexchangeform.fill_third_question), F.text.isdigit)
async def process_third_answer_sent(message: Message, state: FSMContext, session_maker: sessionmaker):
    """
    This handler will be triggered if the data is entered correctly.
    Change the machine state from 'fill_second_question' to 'fill_fourth_question.
    Gives an answer to the user.
    Saves the answers to the exchange_history table.
    '"""

    await state.update_data(tq=message.text)

    user_id = message.from_user.id

    user_data = await state.get_data()
    amount: int = int(user_data['fq'])
    cur1: str = user_data['sq']
    cur2: str = user_data['tq']

    # получаем курс обмена
    ans = await (exchange_rate(amount, cur1, cur2))

    await message.answer(text=f'{amount} {cur1} = {ans} {cur2}')

    # Сохраняем ответы пользователя в историю
    await add_exchange_history(amount, ans, cur1, cur2, user_id, session_maker=session_maker)
    await message.answer(text='Хотите сделать еще один обмен?',
                         reply_markup=create_exchange_keyboard())
    await state.set_state(FSMexchangeform.fill_fourth_question)


@router.callback_query(StateFilter(FSMexchangeform.fill_fourth_question),
                       F.data.in_(['exchange_more']))
async def process_yes_button_sent(callback: CallbackQuery, state: FSMContext):
    """This handler is triggered by pressing the YES button."""

    await callback.message.answer(text='\n\nВведите сумму желаемую к обмену\n\n')
    await state.clear()
    await state.set_state(FSMexchangeform.fill_first_question)


@router.callback_query(StateFilter(FSMexchangeform.fill_fourth_question),
                       F.data.in_(['no_exchange']))
async def process_no_button_sent(callback: CallbackQuery, state: FSMContext):
    """This handler is triggered by pressing the NO button."""

    await callback.message.answer(text='Приходи еще')
    await state.clear()
