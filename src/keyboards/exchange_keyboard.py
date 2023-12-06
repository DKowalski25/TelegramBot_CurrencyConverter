from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def create_exchange_keyboard():
    """Функция генерирующая клавиатуру внутри команды '/exchange'. """
    yes_no_builder = InlineKeyboardBuilder()
    yes_button = InlineKeyboardButton(text='YES',
                                      callback_data='exchange_more')
    no_button = InlineKeyboardButton(text='NO',
                                     callback_data='no_exchange')
    yes_no_builder.row(yes_button, no_button, width=2)

    return yes_no_builder.as_markup()
