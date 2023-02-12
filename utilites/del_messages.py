from . import bot, time, types, DELETE_MESSAGES_TIMER

timer = time()
del_messages_list = []


def del_messages_append(message: types.Message):
    """
    appends (message chat id, message id) to list
    """
    del_messages_list.append((message.chat.id, message.message_id))


async def del_messages():
    """
    Remove messages from chat by message_id, chat_id from list.
    """
    for chat_id, msg_id in del_messages_list:
        try:
            await bot.delete_message(chat_id, msg_id)
        except Exception:
            print("no message")


async def del_msg_by_timer():
    """
    removes via bot messages every 30 mins
    """
    global timer
    if time() - timer > DELETE_MESSAGES_TIMER and del_messages_list:
        await del_messages()
        del_messages_list.clear()
        timer = time()
