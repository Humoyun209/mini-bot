import logging
import asyncio
import aiohttp
from environs import Env

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter

from dbase import DataBase

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state


env = Env()
env.read_env()


bot = Bot(token=env.str('TOKEN'))
dp = Dispatcher()
db = DataBase()
password = env.str('PASSWORD')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - [%(asctime)s] - %(name)s - %(message)s'
)


class InputPassword(StatesGroup):
    input_password = State()
    

async def get_message(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.text('utf-8')


@dp.message(Command(commands=['start']))
async def process_start(message: Message, state: FSMContext):
    user = await db.check_user(message.from_user.id)
    if user is None:
        await state.set_state(InputPassword.input_password)
        await message.answer("Здравствуйте! Для доступа к данным, введите пароль:")
    else:
        await message.answer("Вы можете пользоваться ботом!")


@dp.message(StateFilter(InputPassword.input_password))
async def process_start(message: Message, state: FSMContext):
    if message.text == password:
        await db.insert_user(
            user_id=message.from_user.id,
            username=message.from_user.username
        )
        await message.answer("Поздравляю, вы успешно ввели пароль!")
        await state.set_state(default_state)
    else:
        await message.answer("Пароль неправильно введена!")


@dp.message()
async def send_message(message: Message, bot: Bot):
    # result = await get_message('http://localhost:8000')
    users = await db.user_list()
    for user in users:
        await bot.send_message(user[0], message.text)


if __name__ == '__main__':
    asyncio.run(dp.run_polling(bot))
    

