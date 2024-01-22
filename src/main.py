import asyncio
import logging

from aiogram import Bot, Dispatcher

from database import create_engine, get_session_maker, postgres_url, storage, redis,\
    metadata, BaseModel, proceed_schemas
from utils import config

from .handlers import user_handlers, exchange_handlers
from .keyboards.main_menu import set_main_menu


# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname) -8s '
               '[[%(asctime)s] - %(name)s - %(message)s'
    )

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting Bot')


    # Инициализируем бот и диспетчер
    bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(exchange_handlers.router)

    async_engie = create_engine(postgres_url)
    await proceed_schemas(async_engie, BaseModel.metadata)
    session_maker = get_session_maker(async_engie)

    # dp.storage['session_maker'] = session_maker




    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, session_maker=session_maker, logger=logger, redis=redis)


if __name__ == '__main__':
    asyncio.run(main())
