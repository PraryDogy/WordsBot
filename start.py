import hashlib
from asyncio import sleep

from aiogram import Bot, Dispatcher, executor, types, utils
from aiogram.types import (InlineQuery, InlineQueryResultArticle,
                           InputTextMessageContent)
from aiogram.types.input_file import InputFile

import cfg
from database import Fat, Libera
from dicts import libera, no_libera, you_fat, you_not_fat
from utils import (chat_words, check_user, den_light, inline_test, my_words,
                   president, top_boltunov, words_convert, write_db)

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['my_words'])
async def send_my_words(message: types.Message):
    top = my_words(message.from_user.id, message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=top)


@dp.message_handler(commands=['chat_words'])
async def send_chat_words(message: types.Message):
    top = chat_words(message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=top)


@dp.inline_handler()
async def inline_libera(inline_query: InlineQuery):

    libera_head = 'Насколько я либерал'
    libera_head_id: str = hashlib.md5(libera_head.encode()).hexdigest()

    libera_test_res = inline_test(
        model = Libera,
        msg_user_id = inline_query.from_user.id,
        say='Я либерал на',
        good_phrases=libera,
        bad_phrases=no_libera
        )

    libera_msg = InputTextMessageContent(libera_test_res)

    libera_item = InlineQueryResultArticle(
                id=libera_head_id,
                title=f'{libera_head}',
                input_message_content=libera_msg,
                thumb_url=cfg.PUTIN_IMG
                )

    fat_head = 'Насколько я жирный'
    fat_head_res: str = hashlib.md5(fat_head.encode()).hexdigest()

    fat_test_res = inline_test(
        model = Fat,
        msg_user_id = inline_query.from_user.id,
        say='Я жирный на',
        good_phrases=you_fat,
        bad_phrases=you_not_fat
        )
    fat_msg = InputTextMessageContent(fat_test_res)

    fat_item = InlineQueryResultArticle(
                id=fat_head_res,
                title=f'{fat_head}',
                input_message_content=fat_msg,
                thumb_url=cfg.FAT_IMG
                )

    items = [libera_item, fat_item]

    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)


@dp.inline_handler()
async def inline_fat(inline_query: InlineQuery):

    header = 'Насколько я жирный'
    result_id: str = hashlib.md5(header.encode()).hexdigest()
    
    test = inline_test(
        model = Fat,
        msg_user_id = inline_query.from_user.id,
        say='Я жирный на',
        good_phrases=you_fat,
        bad_phrases=you_not_fat
        )
    msg = InputTextMessageContent(test)

    item = InlineQueryResultArticle(
                id=result_id,
                title=f'{header}',
                input_message_content=msg,
                thumb_url=cfg.FAT_IMG
                )
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)


@dp.message_handler(commands=['top_boltunov'])
async def top_slovobludov(message: types.Message):
    msg = top_boltunov(message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['gde_svet_denis'])
async def get_ava(message: types.Message):
    feu = 536755681
    counter = 0
    while counter < 5:

        try:
            user_photos = await bot.get_user_profile_photos(user_id=feu, limit=1)
            last_photo = dict((user_photos.photos[0][-1])).get("file_id")
            file = await bot.get_file(last_photo)
            counter = 6

        except utils.exceptions.BadRequest:
            await sleep(1)
            user_photos = await bot.get_user_profile_photos(user_id=feu, limit=1)
            last_photo = dict((user_photos.photos[0][-1])).get("file_id")
            counter += 1

    if counter == 5:
        return

    ava = await bot.download_file(file.file_path, './img/ava.png')
    if den_light(ava.name):
        await bot.send_message(chat_id=message.chat.id, text='Света нет :(')
    else:
        await bot.send_message(chat_id=message.chat.id, text='Свет есть!)')


@dp.message_handler()
async def echo(message: types.Message):
    check_user(message.from_user.id, message.from_user.username)
    words_list = words_convert(message.text)

    pres = president(words_list)
    if pres:
        stick = InputFile(pres)
        await bot.send_sticker(
            message.chat.id,
            sticker=stick,
            reply_to_message_id=message.message_id
            )

    write_db(message.from_user.id, message.chat.id, words_list)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)