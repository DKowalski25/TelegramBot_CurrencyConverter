from aiogram.fsm.state import default_state, StatesGroup, State


class FSMexchangeform(StatesGroup):
    """The class used to manage the FSM inside the '/exchange' command."""

    fill_first_question = State()
    fill_second_question = State()
    fill_third_question = State()
    fill_fourth_question = State()


# Создал словарь для взаимодействия с собственными фильтрами (InStatesFilter)
fsm_exchange_form_state: list[str] = ['fill_first_question', 'fill_second_question',
                                      'fill_third_question']
