from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()

# Создаем "базу данных" пользователей
user_answer: dict[int, dict[str, float | int | str ]] = {}


class FSMexchangeform(StatesGroup):
    """ Класс, используемый для управления FSM внутри команды '/exchange'."""
    fill_first_question = State()
    fill_second_question = State()
    fill_third_question = State()
    fill_fourth_question = State()


# Создал словарь для взаимодействия с собственными фильтрами (InStatesFilter)
fsm_exchange_form_state: list[str] = ['fill_first_question', 'fill_second_question',
                                      'fill_third_question']
