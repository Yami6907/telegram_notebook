import asyncio

import re
from datetime import date

from conf import TOKEN
from KeyBoard import main_kb,date_kb

from bd import Database

from aiogram import F
from aiogram import Bot, Dispatcher, types

from aiogram.client.session.aiohttp import AiohttpSession

dp = Dispatcher()
bd = Database()

start_mes = '''
Привет, я бот, который будет делать записи в твой электронный дневник!
Так же я предоставлю тебе список дат, при помощи которых ты сможешь обращаться ко мне.
Тем самым я буду отправлять тебе твои записи в этот день)
Каждое твоё отправленное сообщение будет записываться в дневник.
'''

@dp.message(F.text == '/start')
async def cmd_start(message: types.Message) -> None:
    bd.add_user(message.from_user.id)
    await message.answer(start_mes,reply_markup=main_kb)

@dp.message(F.text == 'Список дат')
async def write_the_date(message: types.Message) -> None:
    s = bd.get_key(message.from_user.id)
    if s is None:
        await message.answer('У вас нет записей. Чтобы добавить запись напишите боту, то что вы бы хотели добавить в дневник.')
    else:
        await message.answer('Ваши дни записи.',reply_markup=date_kb(s))

@dp.message(F.text == 'Меню')
async def main_menu(message: types.Message) -> None:
    await message.answer('Вы перешли в главное меню.',reply_markup=main_kb)

@dp.message(F.text)
async def write_the_record(message: types.Message) -> None:
    if bool(re.match(r'[1-9][0-9]{3}-[0-1][1-9]-[0-3][0-9]',message.text)):
        s = bd.ret_record(re.match(r'[1-9][0-9]{3}-[0-1][1-9]-[0-3][0-9]',message.text).group(),message.from_user.id)
        if not s:
            await message.answer('Такой даты не существует')
        else:
            await message.answer(s)
    else:
        bd.add_record(message.from_user.id,{str(date.today()):message.text})
        await message.answer('Запись добавлена!',reply_markup=main_kb)


async def main() -> None:
    session = AiohttpSession(proxy='http://proxy.server:3128')
    bot = Bot(token=TOKEN, session=session)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
