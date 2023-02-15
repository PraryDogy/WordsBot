from . import bot, time, types, DELETE_MESSAGES_TIMER, datetime, timedelta

timer = time()
del_messages_list = []


def del_messages_append(message: types.Message):
    """
    appends (message chat id, message id) to list
    """
    del_messages_list.append(
        (
            message.chat.id,
            message.message_id,
            datetime.today()
            )
            )


async def del_messages():
    """
    Remove messages from chat by message_id, chat_id from list.
    """
    young_msg = []
    now = datetime.today()

    for chat_id, msg_id, msg_time in del_messages_list:
        try:

            if now - timedelta(hours=1) > msg_time:
                await bot.delete_message(chat_id, msg_id)
            else:
                young_msg.append((chat_id, msg_id, msg_time))

        except Exception:
            print("no message")

    if young_msg:
        del_messages_list.clear()
        del_messages_list.extend(young_msg)


async def del_msg_by_timer():
    """
    removes via bot messages every DELETE_MESSAGES_TIMER seconds
    """
    global timer
    if time() - timer > DELETE_MESSAGES_TIMER and del_messages_list:
        await del_messages()
        del_messages_list.clear()
        timer = time()
