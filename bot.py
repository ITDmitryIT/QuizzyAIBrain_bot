import asyncio
from aiogram import Bot, Dispatcher
from database import create_table
from handlers import router

# Инициализация бота и диспетчера
bot = Bot(token="8182695012:AAHF763LI5pRCxjy0jaL0REGFb52nRbmdHU")  # Замените на ваш токен
dp = Dispatcher()
dp.include_router(router)  # Подключаем роутер с обработчиками

# Запуск бота
async def main():
    await create_table()  # Создаем таблицу при запуске бота
    try:
        print("Бот запущен. Нажмите Ctrl+C для остановки.")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Закрываем сессию бота
        await bot.session.close()
        print("Сессия бота закрыта.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа завершена.")