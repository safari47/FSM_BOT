from msg.msg import NEW_USER_REQUEST_MESSAGE
async def generate_message(data: dict, username: str, name: str) -> str:
    return NEW_USER_REQUEST_MESSAGE.format(
        name=name,
        username=username,
        services=data.get("services", "Не указано"),
        description=data.get("description", "Не указано"),
        deadlines=data.get("deadlines", "Не указано"),
        communication=data.get("communication", "Не указано"),
        phone=data.get("phone", "Не указано"),
    )