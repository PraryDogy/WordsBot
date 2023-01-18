from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import *

from bot_config import TOKEN
from database_queries import *
from text_analyser import *
from utils_handler import *
from utils_inline import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['user_words'])
async def send_my_words(message: types.Message):
    db_user_record(message.from_user.id, message.from_user.username)
    args = message.get_args()
    msg = user_words_top(message.chat.id, message.from_user.username, args)
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['chat_words'])
async def send_chat_words(message: types.Message):
    db_user_record(message.from_user.id, message.from_user.username)
    top = chat_words_top(message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=top)


@dp.message_handler(commands=['top_boltunov'])
async def top_slovobludov(message: types.Message):
    db_user_record(message.from_user.id, message.from_user.username)
    msg = top_boltunov(message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=msg)


# @dp.message_handler(content_types='photo')
# async def get_word_stat(message: types.Message):
#     print(get_file_id(message))


@dp.message_handler(commands=['word_stat'])
async def get_word_stat(message: types.Message):
    db_user_record(message.from_user.id, message.from_user.username)
    args = message.get_args()
    await bot.send_message(message.chat.id, text=word_stat(message.chat.id, args))


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    with open('txt_start.txt', 'r') as file:
        data = file.read()
    await bot.send_message(
        chat_id=message.chat.id,
        text=data,
        )


@dp.inline_handler()
async def inline_libera(inline_query: InlineQuery):
    db_user_record(inline_query.from_user.id, inline_query.from_user.username)

    items = []
    items.append(ItemPokemons(inline_query.from_user.id).item)
    items.append(ItemPuppies(inline_query.from_user.id).item)

    items.append(ItemPenis(inline_query.from_user.id).item)
    items.append(ItemAss(inline_query.from_user.id).item)
    items.append(ItemLibera(inline_query.from_user.id).item)
    items.append(ItemFat(inline_query.from_user.id).item)
    items.append(ItemMobi(inline_query.from_user.id).item)

    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)


@dp.message_handler()
async def echo(message: types.Message):

    # if message.via_bot:
    #     return

    # img = InputMediaPhoto(
    #     media = 'AgACAgIAAx0CYSXtmQACBR5jxSj6C8tQvdZLy0etdc2Y1uk3jgACyMYxG4SkKUosfglEfCzsAQEAAwIAA3gAAy0E',
    #     has_spoiler = True
    # )

    # await bot.send_message(
    #     chat_id = message.chat.id,
    #     photo=img)
    
    # return


    if khalisi_politic(message.text):
        await bot.send_photo(
            message.chat.id,
            photo='AgACAgIAAx0CYSXtmQACBR5jxSj6C8tQvdZLy0etdc2Y1uk3jgACyMYxG4SkKUosfglEfCzsAQEAAwIAA3gAAy0E',
            reply_to_message_id=message.message_id,
            caption=khalisi_convert(message.text)
            )

    if '@prariewords_bot' in message.text and message.chat.id != cfg.heli:
        try:
            await message.delete()
            khalisi_msg = khalisi_convert(message.reply_to_message.text)
            msg_reply_id = message.reply_to_message.message_id
            await bot.send_photo(
                message.chat.id,
                photo='AgACAgIAAx0CYSXtmQACBR5jxSj6C8tQvdZLy0etdc2Y1uk3jgACyMYxG4SkKUosfglEfCzsAQEAAwIAA3gAAy0E',
                reply_to_message_id=msg_reply_id,
                caption=khalisi_msg
                )

        except AttributeError:
            print('no reply')

    db_user_record(message.from_user.id, message.from_user.username)
    db_words_record(message.from_user.id, message.chat.id, words_regex(message.text))


if __name__ == '__main__':
    inp = input(
        'Вы уверены, что сменили токен бота? Напишите любую букву и нажми ввод. Для отмены нажмите только ввод\n')
    if inp:
        Dbase.base.metadata.create_all(Dbase.conn)
        executor.start_polling(dp, skip_updates=True)
