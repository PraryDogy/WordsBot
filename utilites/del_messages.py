from . import bot, time, types, delete_msg_timer

timer = time()
del_messages_list = []


def del_messages_append(message: types.Message):
    del_messages_list.append((message.chat.id, message.message_id))


async def del_messages():
    for chat_id, msg_id in del_messages_list:
        try:
            await bot.delete_message(chat_id, msg_id)
        except Exception:
            print("no message")


async def del_messages_timer():
    """
    removes via bot messages every 30 mins
    """
    global timer
    if time() - timer > delete_msg_timer and del_messages_list:
        await del_messages()
        del_messages_list.clear()
        timer = time()
