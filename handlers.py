from aiogram import types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database import update_quiz_index, get_quiz_index, save_quiz_result, get_quiz_statistics
from keyboards import generate_options_keyboard
from quiz_data import quiz_data
from utils import get_question

# Роутер для обработчиков
from aiogram import Router
router = Router()

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

# Команда /stat
@router.message(Command("stat"))
async def cmd_stat(message: types.Message):
    # Получаем статистику
    statistics = await get_quiz_statistics()
    if statistics:
        # Формируем сообщение со статистикой
        stat_message = "Статистика игроков:\n"
        for username, score in statistics:
            stat_message += f"{username}: {score} баллов\n"
        await message.answer(stat_message)
    else:
        await message.answer("Статистика пока отсутствует.")

# Обработка нажатия на кнопку "Начать игру"
@router.message(lambda message: message.text == "Начать игру")
async def start_quiz(message: types.Message):
    user_id = message.from_user.id
    await update_quiz_index(user_id, 0)  # Сбрасываем индекс вопроса
    await get_question(message, user_id)  # Задаем первый вопрос

# Обработка ответа (правильного или неправильного)
@router.callback_query(F.data.startswith("answer_"))
async def handle_answer(callback: types.CallbackQuery):
    # Разбираем callback_data
    data = callback.data.split("_")
    selected_option_index = int(data[1])  # Индекс выбранного ответа
    correct_option_index = int(data[2])   # Индекс правильного ответа

    # Получаем текст выбранного ответа
    selected_option = quiz_data[await get_quiz_index(callback.from_user.id)]['options'][selected_option_index]
    correct_option = quiz_data[await get_quiz_index(callback.from_user.id)]['options'][correct_option_index]

    # Убираем кнопки
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Отправляем в чат текст выбранного ответа
    await callback.message.answer(f"Вы выбрали: {selected_option}")

    # Проверяем, правильный ли ответ
    if selected_option_index == correct_option_index:
        await callback.message.answer("Верно! 🎉")
    else:
        await callback.message.answer(f"Неправильно. Правильный ответ: {correct_option}")

    # Обновляем индекс вопроса
    user_id = callback.from_user.id
    current_question_index = await get_quiz_index(user_id)
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)

    # Задаем следующий вопрос или завершаем квиз
    if current_question_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        # Сохраняем результат
        username = callback.from_user.username or callback.from_user.first_name
        await save_quiz_result(user_id, username, current_question_index)  # Сохраняем текущий балл
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")