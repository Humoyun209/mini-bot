import logging
import asyncio
import random
from environs import Env

from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state

from dbase import DataBase




env = Env()
env.read_env()


bot = Bot(token=env.str('TOKEN'))
dp = Dispatcher()

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - [%(asctime)s] - %(name)s - %(message)s'
)

db = DataBase()

password = env.str('PASSWORD')

class InputPassword(StatesGroup):
    input_password = State()


@dp.message(Command(commands=['start']))
async def process_start(message: Message, state: FSMContext):
    user = await db.check_user(message.from_user.id)
    logging.info(f'Пользователь {message.from_user.username} начал пользоваться ботом')
    if user is None:
        await state.set_state(InputPassword.input_password)
        await message.answer("Здравствуйте! Для доступа к данным, введите пароль:")
    else:
        await message.answer("Вы можете пользоваться ботом!")


@dp.message(Command(commands=['stop']))
async def process_stop(message: Message):
    logging.info(f'Пользователь {message.from_user.username} отписался')
    await db.delete_user(message.from_user.id)
    await message.answer("Вы отписались! Начать /start")


@dp.message(StateFilter(InputPassword.input_password))
async def process_start(message: Message, state: FSMContext):
    if message.text == password:
        username = message.from_user.username
        await db.insert_user(
            user_id=message.from_user.id,
            username= username if username else f'Anonym{random.randint(1, 1000000)}'
        )
       
        await message.answer("Поздравляю, вы успешно ввели пароль!")
        logging.info(f'Пользователь {message.from_user.username} подписался')
        await state.set_state(default_state)
    else:
        await message.answer("Пароль неправильно введена!")
        logging.info(f'Пользователь {message.from_user.username} неправильно ввел пароль')


async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    
    
