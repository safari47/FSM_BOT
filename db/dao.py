from .base import connection
from .models import User
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger


@connection()
async def add_user(session, user_id: int, first_name: str, last_name: str, username: str):
    try:
        new_user = User(telegram_id=user_id, first_name=first_name, last_name=last_name, username=username)
        session.add(new_user)
        await session.commit()
        return new_user
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        await session.rollback()


@connection()
async def get_user(session, user_id: int):
    try:
        user = await session.scalar(select(User).filter_by(telegram_id=user_id))
        return user
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении пользователя: {e}")
        return None

@connection()
async def get_all_users(session):
    try:
        result = []
        users = await session.execute(select(User))
        user_list = users.scalars().all()
        for user in user_list:
            telegram_id, first_name, last_name, username = map(
                str,
                (
                    user.telegram_id,
                    user.first_name,
                    user.last_name,
                    user.username,
                ),
            )
            result.append(
                {
                    "telegram_id": telegram_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                }
            )

        return result
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении канала: {e}")
        await session.rollback()