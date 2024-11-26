from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from config.config import bot, settings
from aiogram.fsm.context import FSMContext
from fsm.fsm import Request
from config.config import settings
from keyboards.keyboards import (
    phone_number,
    user_kb,
    services,
    back_to,
    confirm,
    inline_user_contact,
)
from msg.msg import (
    services_title,
    CANCEL_ACTION,
    SELECT_SERVICE,
    INVALID_SERVICE_SELECTION,
    PROJECT_DESCRIPTION_PROMPT,
    PROJECT_DEADLINE_PROMPT,
    SEND_PHONE_PROMPT,
    INVALID_PHONE_PROMPT,
    CONFIRM_PROMPT,
    REQUEST_SUMMARY,
    APPLICATION_CANCELLED,
    APPLICATION_SENT,
    COMMUNICATION_PROMPT
)
from utils.utils import generate_message

router = Router()


@router.message(F.text == "❌ ОТМЕНА")
async def cancel_action(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(CANCEL_ACTION, reply_markup=ReplyKeyboardRemove())
    await message.answer(
        "🔄 Вы вернулись в главное меню.", reply_markup=user_kb(message.from_user.id)
    )


# Обработчик для кнопки "НОВАЯ ЗАЯВКА"
@router.callback_query(F.data == "new_call")
async def get_services(call: CallbackQuery, state: FSMContext):
    await call.message.answer(SELECT_SERVICE, reply_markup=services())
    await state.set_state(Request.services)


@router.message(Request.services)
async def handle_services(message: Message, state: FSMContext):
    service = message.text
    if service not in services_title:
        await message.answer(INVALID_SERVICE_SELECTION, reply_markup=services())
        return
    await state.update_data(services=service)
    await message.answer(PROJECT_DESCRIPTION_PROMPT, reply_markup=back_to())
    await state.set_state(Request.description)


@router.message(Request.description)
async def handle_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(PROJECT_DEADLINE_PROMPT, reply_markup=back_to())
    await state.set_state(Request.deadlines)


@router.message(Request.deadlines)
async def handle_deadlines(message: Message, state: FSMContext):
    await state.update_data(deadlines=message.text)
    await message.answer(COMMUNICATION_PROMPT) 
    await state.set_state(Request.communication)

@router.message(Request.communication)
async def handle_communication(message: Message, state: FSMContext):
    await state.update_data(communication=message.text)
    await message.answer(SEND_PHONE_PROMPT, reply_markup=phone_number())
    await state.set_state(Request.phone)


@router.message(Request.phone)
async def handle_phone(message: Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
        await state.update_data(phone=phone)
    else:
        await message.answer(INVALID_PHONE_PROMPT, reply_markup=phone_number())
        return

    request_data = await state.get_data()
    message_text = REQUEST_SUMMARY.format(
        name=message.from_user.first_name,
        username=message.from_user.username,
        services=request_data["services"],
        description=request_data["description"],
        deadlines=request_data["deadlines"],
        phone=request_data["phone"],
    )

    await message.answer(message_text)
    await message.answer(CONFIRM_PROMPT, reply_markup=confirm())
    await state.set_state(Request.confirmation)


@router.message(Request.confirmation)
async def handle_confirmation(message: Message, state: FSMContext):
    conf = message.text
    if conf == "✅ ДА":
        await message.answer(APPLICATION_SENT, reply_markup=ReplyKeyboardRemove())
        await message.answer(text="🔄 Вы вернулись в главное меню.", reply_markup=user_kb(message.from_user.id),)
        request_data = await state.get_data()
        message_text = await generate_message(
            data=request_data,
            username=message.from_user.username,
            name=message.from_user.first_name,
        )
        button = inline_user_contact(message.from_user.username)
        await bot.send_message(settings.ADMIN_ID, message_text, reply_markup=button)
        await state.clear()
    else:
        await message.answer(APPLICATION_CANCELLED, reply_markup=ReplyKeyboardRemove())
        await message.answer(text="🔄 Вы вернулись в главное меню.", reply_markup=user_kb(message.from_user.id))
        await state.clear()
