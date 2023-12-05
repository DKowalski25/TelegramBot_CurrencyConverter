from abc import ABC

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class InStatesFilter(BaseFilter, ABC):
    """Фильтр проверяет находиться ли FSM в одном из состояний 'fsm_exchange_form_state'. """

    def __init__(self, states: list[str]) -> None:
        self.states = states

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        fms_state = await state.get_state()
        state_name = fms_state.split(':')[1]
        return state_name in self.states


class CheckingLetterCode(BaseFilter, ABC):
    """Фильтр проверяет чтоб приходящие значение совпадает с принятым форматом
     обозначения валют. """

    async def __call__(self, message: Message) -> bool:
        data = message.text
        return data.isalpha() and data.isupper and len(data) == 3
