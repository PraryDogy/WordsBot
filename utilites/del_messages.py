from . import bot, time, types, wraps, delete_msg_timer

timer = time()
for_delete = []


def for_delete_append(message: types.Message):
    for_delete.append((message.chat.id, message.message_id))


async def del_messages():
    for chat_id, msg_id in for_delete:
        try:
            await bot.delete_message(chat_id, msg_id)
        except Exception:
            print("no message")


async def del_messages_timer():
    """
    removes via bot messages every 30 mins
    """
    global timer
    if time() - timer > delete_msg_timer and for_delete:
        print("delete by timer")
        await del_messages()
        for_delete.clear()
        timer = time()
