from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

CURRENCY_CODE_LEN = 3


class InStatesFilter(BaseFilter):
    """The filter checks whether the FSM is in one of the 'fsm_exchange_form_state' states."""

    def __init__(self, states: list[str]) -> None:
        self.states = states

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        fms_state = await state.get_state()
        state_name = fms_state.split(':')[1]
        return state_name in self.states


class CheckingLetterCode(BaseFilter):
    """
    The filter checks that the incoming value matches the accepted format
    currency designations.
    """

    async def __call__(self, message: Message) -> bool:
        data = message.text
        return data.isalpha() and data.isupper and len(data) == CURRENCY_CODE_LEN
