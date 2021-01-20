"""
This is a DLS_Alexk bot.

It can do a lot of things.

And echoes any incoming text messages.
"""

import logging
import os

from aiogram import Bot, Dispatcher, executor, types

from aiogram.dispatcher.filters.state import State, StatesGroup
#from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram.contrib.fsm_storage.memory import MemoryStorage

# write your telegram bot token here
API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class GetPictures(StatesGroup):
    waiting_for_style_picture = State()
    waiting_for_content_picture = State()


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.reply("Hi!\nI'm DLS_Alexk bot!\nPowered by aiogram.\nUse /help to see what I can.")


@dp.message_handler(commands=['help'], state="*")
async def send_help(message: types.Message):
    """
    This handler will be called when user sends `/help` command
    """
    await message.reply("/style - загрузить картинку стиля;\n/content - загрузить картинку контента;\n/work - запустить перенос стиля на контент;\n/date - дата и время;\n/month - календарь текущего месяца;\n/uptime - uptime сервера с ботом;\n/weather - погода в Орле;\n/weatherl - погода в Орле (одной строкой).\n")


@dp.message_handler(commands=['date'], state="*")
async def send_date(message: types.Message):
    cdate = os.popen('date').read()
    await message.reply(cdate)


@dp.message_handler(commands=['month'], state="*")
async def send_month(message: types.Message):
    cmonth = os.popen('cal').read()
    await message.reply(cmonth)


@dp.message_handler(commands=['uptime'], state="*")
async def send_uptime(message: types.Message):
    cmonth = os.popen('uptime').read()
    await message.reply(cmonth)


@dp.message_handler(commands=['uname'], state="*")
async def send_uname(message: types.Message):
    un = os.popen('uname -a').read()
    await message.reply(un)


@dp.message_handler(commands=['weatherl'], state="*")
async def send_w(message: types.Message):
    wl = os.popen('curl -s "http://wttr.in/Orel?lang=fr&format=%l:+%c:%C+%t+%h+%w+%m"').read()
    await message.reply(wl)


@dp.message_handler(commands=['weather'], state="*")
async def send_wl(message: types.Message):
    os.system('wget -q http://wttr.in/Orel_0tqp_lang=fr.png -O Orel.png')
    with open('Orel.png', 'rb') as photo:
        await message.reply_photo(photo, caption='🌡️')


@dp.message_handler(commands="style", state="*")
async def get_style_step_1(message: types.Message):
    await message.answer("Загрузите картинку стиля:")
    await GetPictures.waiting_for_style_picture.set()


@dp.message_handler(state=GetPictures.waiting_for_style_picture, content_types=types.ContentTypes.PHOTO) 
async def get_style_step_2(message):
    await message.answer("Результат работы команды /style: загружена картинка style.jpg")
    await message.photo[0].download('style.jpg')


@dp.message_handler(commands="content", state="*")
async def get_content_step_1(message: types.Message):
    await message.answer("Загрузите картинку контента:")
    await GetPictures.waiting_for_content_picture.set()


@dp.message_handler(state=GetPictures.waiting_for_content_picture, content_types=types.ContentTypes.PHOTO)
async def get_content_step_2(message):
    await message.answer("Результат работы команды /content: загружена картинка content.jpg")
    await message.photo[0].download('content.jpg')


@dp.message_handler(commands="work", state="*")
async def execute_model(message: types.Message):
    await message.reply("Запускаю перенос стиля...")
    await message.reply("Ожидайте 5 минут.")
    os.system('python3 gdrive/MyDrive/nst/nst.py style.jpg content.jpg')
    with open('output.png', 'rb') as photo:
        await message.reply_photo(photo, caption='результат переноса стиля на контент')
    os.remove('style.jpg')
    os.remove('content.jpg')
    os.remove('output.png')
    await message.reply("Результат работы команды /work: вам показан перенесённый стиль, все загруженные ранее картинки удалены.")

@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        '''
        # Old fashioned way:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption='Cats are here 😺',
            reply_to_message_id=message.message_id,
        )
        '''

        await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
