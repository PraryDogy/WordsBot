from aiogram import types

from bot_config import bot


async def send_msg(message: types.Message):
    with open('handlers_msg/txt_start.txt', 'r') as file:
        data = file.read()
    await bot.send_message(chat_id=message.chat.id, text=data)