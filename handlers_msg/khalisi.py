from . import bot, khalisi_convert, types
import links

__all__ = (
    "send_msg"
    )


async def send_msg(message: types.Message):
    try:
        msg: str = message.reply_to_message.text

        khalisied = khalisi_convert(msg.lower().split())
        msg = " ".join(khalisied).capitalize()

        await bot.send_photo(
            message.chat.id,
            photo=links.khalisi,
            reply_to_message_id=message.reply_to_message.message_id,
            caption=msg
            )

    except AttributeError:
        await bot.send_photo(
            chat_id = message.chat.id,
            photo = links.khalisi_err,
            caption = "Вызовите Кхалиси с реплаем сообщения.",
            reply_to_message_id = message.message_id
            )
        return