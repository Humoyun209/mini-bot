from urllib.parse import unquote
import aiohttp
from aiohttp import web
from environs import Env

import asyncio
from dbase import DataBase
from dbase import DataBase


db = DataBase()
env = Env()
env.read_env()

async def send_message(user_id, message):
    url = f"https://api.telegram.org/bot{env.str('TOKEN')}/sendMessage"
    params = {
        'chat_id': user_id,
        'text': message
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return response.status


async def main(message: str, users: list):
    tasks = []
    for user in users:
        tasks.append(
            asyncio.create_task(send_message(user[0], message))
        )
    result = await asyncio.gather(*tasks)
    print(f'Сообщение успешно отправлено - {result.count(200)} юзерам из {len(result)} юзеров')
        

async def handle(request):
    queries = request.url.query
    db = DataBase()
    users = await db.user_list()
    if len(queries):
        message = unquote(queries.get('text'), encoding='utf-8')
        if message:
            await main(message, users)
    return web.Response(text="Сервер работает!")

app = web.Application()
app.router.add_get('/', handle)

if __name__ == '__main__':
    web.run_app(app)