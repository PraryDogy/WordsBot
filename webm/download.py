import os

import ffmpeg
from aiogram import types

import links
from bot_config import bot
import traceback

def convert_video(file):

    name, ext = os.path.splitext(file)
    out_name = name + ".mp4"
    ffmpeg.input(file).output(out_name, loglevel = "quiet").overwrite_output().run()

    return out_name


async def send_msg(message: types.Message):
    try:

        try:
            file_id = message.reply_to_message.document.file_id
            file_name = message.reply_to_message.document.file_name
        except (Exception, AttributeError) as ex:
            file_id = message.reply_to_message.video.file_id
            file_name = message.reply_to_message.video.file_name
            print(ex)

        msg = await bot.send_video(
            chat_id = message.chat.id,
            video = open("./webm/cat-typing.mp4", "rb"),
            reply_to_message_id = message.message_id,
            caption = "Работаю"
            )

        try:
            file = await bot.get_file(file_id)
        except Exception:
            await msg.delete()
            await bot.send_message(
                chat_id = message.chat.id,
                text="Файл больше 20мб",
                reply_to_message_id = message.message_id
                )
            return

        file_path = file.file_path

        await bot.download_file(file_path, f"./webm/{file_name}")

        if not file_name.endswith(".mp4"):
            new_name = convert_video(f"./webm/{file_name}")
            new_file = types.InputMediaVideo(open(new_name, "rb"))
        else:
            new_file = types.InputMediaVideo(open(f"./webm/{file_name}", "rb"))

        await msg.edit_media(new_file)

        for i in os.listdir("./webm"):
            if i.endswith((".mp4", ".webm")) and i != "cat-typing.mp4":
                os.remove(os.path.join("./webm", i))

    except Exception as e:
        print(traceback.format_exc())
        await bot.send_photo(
            chat_id = message.chat.id,
            photo=links.video_err,
            caption = "Пришлите видео с реплаем.",
            reply_to_message_id = message.message_id
            )

