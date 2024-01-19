import asyncio
import aiosqlite


class DataBase:
    async def check_user(self, user_id):
        async with aiosqlite.connect('db.sqlite3') as conn:
            user = await conn.execute("SELECT * FROM users WHERE id = ?", (user_id, ))
            return await user.fetchone()
    
    async def insert_user(self, user_id, username):
        async with aiosqlite.connect('db.sqlite3') as conn:
            if not await self.check_user(user_id):
                await conn.execute("INSERT INTO users VALUES(?, ?)", (user_id, username))
                await conn.commit()
    
    async def user_list(self):
        async with aiosqlite.connect('db.sqlite3') as conn:
            users = await conn.execute('SELECT * FROM users')
            return await users.fetchall()

    async def delete_user(self, user_id):
        async with aiosqlite.connect('db.sqlite3') as conn:
            if await self.check_user(user_id):
                await conn.execute('DELETE FROM users WHERE id = ?', (user_id, ))
                await conn.commit()
                

# async def main():
#     db = DataBase()
#     await db.insert_user(2106991711, 'humoyun209')

# asyncio.run(main())