from . import bot, types



async def send_msg(message: types.Message):
    await bot.send_photo(
                chat_id=message.chat.id,
                photo=(
                    "https://sun9-59.userapi.com/impg/6UiAPL_HLp8MKR4mJCU"
                    "8zcvBFiXs3DUyvEwllg/4N3bdDhWxE4.jpg?size=399x352&quali"
                    "ty=95&sign=c45025f8bfe38c8a54f627665a5c592e&type=album"
                    ),
                caption=")))))",
                reply_to_message_id=message.message_id
                )