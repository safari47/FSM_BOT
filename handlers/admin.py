from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile,CallbackQuery
from loguru import logger
from config.config import settings
from db.dao import get_all_users
import json
from keyboards.keyboards import admin_kb
router=Router()

# Callback на клавишу "Управление каналами"
@router.callback_query(F.data == "manage_channels", F.from_user.id == settings.ADMIN_ID)
async def admin_manage_channels(call: CallbackQuery):
    await call.message.answer(text="Список пользователей:", reply_markup=admin_kb())

# Получение списка пользователей и отправка файла
@router.message(F.text == '👥 СПИСОК ПОЛЬЗОВАТЕЛЕЙ', F.from_user.id == settings.ADMIN_ID)
async def get_users(message: Message):
    try:
        user_data = await get_all_users()  # Получаем список пользователей из базы данных
        users_json = json.dumps(user_data, indent=4, ensure_ascii=False)  # Конвертируем в JSON
        # Создаем файл из строки
        data = BufferedInputFile(
            file=users_json.encode("utf-8"),
            filename="users_data.json"
        )
        # Отправляем JSON файл
        await message.answer_document(document=data, caption="👥 СПИСОК ВСЕХ ПОЛЬЗОВАТЕЛЕЙ ИЗ БАЗЫ")
    except Exception as e:
        # Логируем ошибку
        logger.error(f"Ошибка при получении и отправке данных пользователей: {e}")
        await message.answer("Произошла ошибка при обработке данных, попробуйте позже.")
