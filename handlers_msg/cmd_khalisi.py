from bot_config import bot
from utilites import khalisi_convert
from aiogram import types

async def send_msg(message: types.Message):
    try:
        msg: str = message.reply_to_message.text
    except AttributeError:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=(
                "https://sun9-8.userapi.com/impg/"
                "o4h0YbL0OvfSp2_gpy7ZpQgeWAh2lBxMCZ-tQQ/yAnd91aXzvI.jpg"
                "?size=656x332&quality=95&sign=6b3582556c89078e"
                "48fc0f08f03a8347&type=album"
                ),
            caption="Вызовите Кхалиси с реплаем сообщения.",
            reply_to_message_id=message.message_id
            )
        return

    msg = ' '.join(
        khalisi_convert(
            msg.lower().split()
            )
            ).capitalize()

    await bot.send_photo(
        message.chat.id,
        photo=(
            "https://sun9-12.userapi.com/impg/oOGXM3AEHzVrTR77mtSmGE8HzRzb9"
            "_EN09z-0Q/OP2uh8gxsT4.jpg?size=460x300&quality=95&sign=ed7f5d437"
            "785ea571d4d95c5762c5c1f&type=album"
            ),
        reply_to_message_id=message.reply_to_message.message_id,
        caption=msg
        )
