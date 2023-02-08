from . import types, bot, time, wraps

timer = time()
for_delete = []

def del_msg():
    for chat_id, msg_id in for_delete:
        bot.edit_message_media(
            chat_id = chat_id,
            message_id= msg_id,
            media=types.InputMediaPhoto()
        )


def del_message_append(message: types.Message):
    for_delete.append((message.chat.id, message.message_id))


async def del_messages():
    for chat_id, msg_id in for_delete:
        await bot.delete_message(chat_id, msg_id)


async def del_messages_timer():
    global timer
    if time() - timer > 1800 and for_delete:
        await del_messages()
        for_delete.clear()
        timer = time()
