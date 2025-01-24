from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Генерация клавиатуры с вариантами ответов
def generate_options_keyboard(answer_options, correct_option_index):
    builder = InlineKeyboardBuilder()
    for index, option in enumerate(answer_options):
        # Передаем индекс ответа и индекс правильного ответа в callback_data
        builder.add(InlineKeyboardButton(
            text=option,
            callback_data=f"answer_{index}_{correct_option_index}"
        ))
    builder.adjust(1)  # Выводим по одной кнопке в столбик
    return builder.as_markup()