from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from db.dao import get_user, add_user
from keyboards.keyboards import user_kb
from msg.msg import start_msg, repeat_msg
from config.config import settings

router = Router()


# Функция для реагирования на команду /start
@router.message(CommandStart())
async def start(message: Message, command: CommandObject):

    user_data = await get_user(user_id=message.from_user.id)
    if user_data is None:
        await add_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )

    await message.answer(
        text=start_msg.format(username=message.from_user.first_name),
        reply_markup=user_kb(message.from_user.id),
    )



