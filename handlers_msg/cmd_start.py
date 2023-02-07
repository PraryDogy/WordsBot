from . import bot, types

__all__ = (
    "send_msg"
    )


async def send_msg(message: types.Message):
    with open('handlers_msg/txt_start.txt', 'r') as file:
        data = file.read()
    await bot.send_message(chat_id=message.chat.id, text=data)