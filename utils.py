from database import get_quiz_index
from quiz_data import quiz_data
from keyboards import generate_options_keyboard

# Функция для задания вопроса
async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    if current_question_index < len(quiz_data):
        question_data = quiz_data[current_question_index]
        question = question_data['question']
        options = question_data['options']
        correct_option_index = question_data['correct_option']
        keyboard = generate_options_keyboard(options, correct_option_index)
        await message.answer(f"Вопрос {current_question_index + 1}: {question}", reply_markup=keyboard)
    else:
        await message.answer("Это был последний вопрос. Квиз завершен!")