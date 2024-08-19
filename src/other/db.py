import aiosqlite

db = 'src/config/data.db'


async def init_db() -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS Staff(
            id INTEGER PRIMARY KEY,
            username CHAR(32)
            )""")

            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students(
            id INTEGER PRIMARY KEY,
            username CHAR(32)
            )""")

            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS Links(
            code CHAR(16),
            purpose CHAR(8) PRIMARY KEY,
            timestamp BIGINT,
            join_count INTEGER
            )""")

            await conn.commit()


async def get_staff(user_id: int = None) -> tuple[tuple]:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = 'SELECT * FROM Staff'
            if user_id:
                req += f' WHERE id = {user_id}'
            await cursor.execute(req)
            return await cursor.fetchall()


async def get_students(user_id: int = None) -> tuple[tuple]:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = 'SELECT * FROM Students'
            if user_id:
                req += f' WHERE id = {user_id}'
            await cursor.execute(req)
            return await cursor.fetchall()


async def get_users() -> tuple[tuple]:
    async with (aiosqlite.connect(db) as conn):
        async with conn.cursor() as cursor:
            return await (await cursor.execute('SELECT * FROM Staff;')).fetchall() + \
                await (await cursor.execute('SELECT * FROM Students;')).fetchall()


async def add_staff(user_id: int, username: str) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            INSERT INTO Staff(id, username)
            VALUES(?, ?)""", (user_id, username,))
            await conn.commit()


async def add_student(user_id: int, username: str) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            INSERT INTO Students(id, username)
            VALUES(?, ?)""", (user_id, username,))
            await conn.commit()


async def delete_staff(user_id: int = None, entire: bool = False) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = "DELETE FROM Staff"
            if not entire:
                req += f" WHERE id = {user_id}"
            elif entire and user_id:
                req += f" WHERE id != {user_id}"

            await cursor.executescript(req)
            await conn.commit()


async def delete_student(user_id: int = None, entire: bool = False) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = "DELETE FROM Students"
            if not entire:
                req += f" WHERE id = {user_id}"
            elif entire and user_id:
                req += f" WHERE id != {user_id}"
            await cursor.executescript(req)
            await conn.commit()


async def staff_check(user_id: int) -> bool:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            SELECT * FROM Staff WHERE id = ?""", (user_id,))
            return bool(await cursor.fetchone())


async def student_check(user_id: int) -> bool:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            SELECT * FROM Students WHERE id = ?""", (user_id,))
            return bool(await cursor.fetchone())


async def link_code_add(code: str, purpose: str, timestamp: int) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            REPLACE INTO Links(code, purpose, timestamp, join_count)
            VALUES(?, ?, ?, 0)""", (code, purpose, timestamp,))
            await conn.commit()


async def link_code_delete(purpose: str) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            DELETE FROM Links WHERE purpose = ?""", (purpose,))
            await conn.commit()


async def link_code_get(purpose: str) -> tuple:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            SELECT code, timestamp, join_count FROM Links WHERE purpose = ?""", (purpose,))
            return await cursor.fetchone()


async def link_code_check(code: str) -> str | bool:
    if not code:
        return False
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            SELECT purpose FROM Links WHERE code = ?""", (code,))
            return await cursor.fetchone()


async def link_code_join(code: str) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            UPDATE Links SET join_count = join_count + 1 WHERE code = ?""", (code,))
            await conn.commit()
