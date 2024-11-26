from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from config.config import settings
from msg.msg import services_title

ADMIN_ID = settings.ADMIN_ID


def user_kb(user_id: id):
    keyboard = [[InlineKeyboardButton(text="📩 НОВАЯ ЗАЯВКА", callback_data="new_call")]]
    if user_id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton(text="⚙️ АДМИНКА", callback_data="manage_channels")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def phone_number():
    buttons = [[KeyboardButton(text="📲 ОТПРАВИТЬ НОМЕР", request_contact=True)]]
    buttons.append([KeyboardButton(text="❌ ОТМЕНА")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Поделитесь номером",
    )
    return keyboard


def services():
    buttons = []
    for service in services_title:
        buttons.append(
            KeyboardButton(text=service)
        )  # Добавляем каждую кнопку в общий список
    # Добавляем кнопку "❌ ОТМЕНА" в конец списка
    buttons.append(KeyboardButton(text="❌ ОТМЕНА"))
    # Группируем кнопки по 2 в строке
    grouped_buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    # Создаем клавиатуру
    keyboard = ReplyKeyboardMarkup(
        keyboard=grouped_buttons,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите услугу",
    )
    return keyboard


def back_to():
    buttons = [[KeyboardButton(text="❌ ОТМЕНА")]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Вернуться назад",
    )
    return keyboard

def confirm():
    buttons = [[KeyboardButton(text="✅ ДА"), KeyboardButton(text="❌ НЕТ")]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Подтвердить",
    )
    return keyboard

def inline_user_contact(username: str) -> InlineKeyboardMarkup:
    # Создаем кнопку с ссылкой на чат пользователя
    button = [[InlineKeyboardButton(text="💭 ОТКРЫТЬ ЧАТ", url=f"https://t.me/@{username}")]]
    return InlineKeyboardMarkup(inline_keyboard=button)

def admin_kb():
    buttons = [[KeyboardButton(text="👥 СПИСОК ПОЛЬЗОВАТЕЛЕЙ")]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выгружает JSON",
    )
    return keyboard