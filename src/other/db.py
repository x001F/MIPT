import aiosqlite


db = 'src/config/data.db'


async def init_db() -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS Admins(
            id INTEGER PRIMARY KEY,
            full_name CHAR(150),
            username CHAR(32)
            )""")

            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS Instructors(
            id INTEGER PRIMARY KEY,
            team_id INTEGER,
            full_name CHAR(150),
            username CHAR(32),
            phone_number INTEGER
            )""")

            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students(
            id INTEGER PRIMARY KEY,
            team_id INTEGER,
            full_name CHAR(150),
            username CHAR(32),
            phone_number INTEGER
            )""")

            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS Rating(
            id INTEGER PRIMARY KEY,
            quark_count INTEGER
            )""")

            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS Unverified(
            id INTEGER PRIMARY KEY,
            full_name CHAR(150),
            username CHAR(32),
            phone_number INTEGER,
            timestamp BIGINT
            )""")

            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY,
            full_name CHAR(150),
            username CHAR(32),
            phone_number INTEGER,
            timestamp BIGINT
            )""")

            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS BlackList(
            id INTEGER PRIMARY KEY,
            timestamp BIGINT
            )""")

            await conn.commit()


async def get_admins(user_id: int = None) -> tuple[tuple]:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = 'SELECT * FROM Admins'
            if user_id:
                req += f' WHERE id = {user_id}'
            await cursor.execute(req)
            return await cursor.fetchall()


async def get_instructors(user_id: int = None) -> tuple[tuple]:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = 'SELECT * FROM Instructors'
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


async def get_rating(team_id: int = None) -> tuple[tuple]:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = 'SELECT * FROM Rating'
            if team_id:
                req += f' WHERE id = {team_id}'
            await cursor.execute(req)
            return await cursor.fetchall()


async def get_recent_users(user_id: int = None) -> tuple[tuple]:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = 'SELECT * FROM Users'
            if user_id:
                req += f' WHERE id = {user_id}'
            await cursor.execute(req)
            return await cursor.fetchall()


async def get_blacklist(user_id: int = None) -> tuple[tuple]:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = 'SELECT * FROM BlackList'
            if user_id:
                req += f' WHERE id = {user_id}'
            await cursor.execute(req)
            return await cursor.fetchall()


async def add_admin(user_id: int, full_name: str, username: str) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            INSERT INTO Admins(id, full_name, username)
            VALUES(?, ?, ?)""", (user_id, full_name, username))
            await conn.commit()


async def add_instructor(user_id: int, team_id: int, full_name: str, username: str, phone_number: int | None) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            INSERT INTO Instructors(id, team_id, full_name, username, phone_number)
            VALUES(?, ?, ?, ?, ?)""", (user_id, team_id, full_name, username, phone_number,))
            await conn.commit()


async def add_student(user_id: int, team_id: int, full_name: str, username: str, phone_number: int | None
                      ) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            INSERT INTO Students(id, team_id, full_name, username, phone_number)
            VALUES(?, ?, ?, ?, ?)""", (user_id, team_id, full_name, username, phone_number,))
            await conn.commit()


async def delete_admin(user_id: int = None, entire: bool = False) -> None:
    if not bool(user_id) and not entire:
        raise UserWarning('The user ID to delete is not specified, or the "entire" parameter')
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = "DELETE FROM Admins"
            if not entire:
                req += f" WHERE id = {user_id}"

            await cursor.executescript(req)
            await conn.commit()


async def delete_instructor(user_id: int = None, entire: bool = False) -> None:
    if not bool(user_id) and not entire:
        raise UserWarning('The user ID to delete is not specified, or the "entire" parameter')
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = "DELETE FROM Instructors"
            if not entire:
                req += f" WHERE id = {user_id}"

            await cursor.executescript(req)
            await conn.commit()


async def delete_student(user_id: int = None, entire: bool = False) -> None:
    if not bool(user_id) and not entire:
        raise UserWarning('The user ID to delete is not specified, or the "entire" parameter')
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = "DELETE FROM Students"
            if not entire:
                req += f" WHERE id = {user_id}"

            await cursor.executescript(req)
            await conn.commit()


async def admin_check(user_id: int) -> bool:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            SELECT * FROM Admins WHERE id = ?""", (user_id,))
            return bool(await cursor.fetchone())


async def instructor_check(user_id: int) -> bool:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            SELECT * FROM Instructors WHERE id = ?""", (user_id,))
            return bool(await cursor.fetchone())


async def stuff_check(user_id: int) -> bool:
    return await admin_check(user_id) or await instructor_check(user_id)


async def student_check(user_id: int) -> bool:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            SELECT * FROM Students WHERE id = ?""", (user_id,))
            return bool(await cursor.fetchone())


async def random_check(user_id: int) -> bool:
    for check in (admin_check, instructor_check, student_check):
        if await check(user_id):
            return True
    return False


async def block_check(user_id: int) -> bool:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            SELECT * FROM BlackList WHERE id = ?""", (user_id,))
            return not bool(await cursor.fetchone())


async def edit_rating(edited_rating: list[tuple]) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.executemany("""
            REPLACE INTO Rating(id, quark_count) 
            VALUES(?, ?)""", edited_rating)
            await conn.commit()


async def delete_rating(team_id: int = None, entire: bool = False) -> None:
    if not bool(team_id) and not entire:
        raise UserWarning('The team ID to delete is not specified, or the "entire" parameter')
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = "DELETE FROM Rating"
            if not entire:
                req += f" WHERE id = {team_id}"

            await cursor.executescript(req)
            await conn.commit()


async def apply_for_verification(user_id: int, full_name: str, username: str, phone_number: int, timestamp: int
                                 ) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            INSERT INTO Unverified(id, full_name, username, phone_number, timestamp) 
            VALUES(?, ?, ?, ?, ?)""", (user_id, full_name, username, phone_number, timestamp,))
            await conn.commit()


async def add_user(user_id: int, full_name: str, username: str, phone_number: int, timestamp: int) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            REPLACE INTO Users(id, full_name, username, phone_number, timestamp) 
            VALUES(?, ?, ?, ?, ?)""", (user_id, full_name, username, phone_number, timestamp,))
            await conn.commit()


async def delete_user(user_id: int) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            DELETE FROM Users WHERE id = ?""", (user_id,))
            await conn.commit()


async def block(user_id: int, timestamp: int) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            REPLACE INTO BlackList(id, timestamp) 
            VALUES(?, ?)""", (user_id, timestamp,))
            await conn.commit()


async def unblock(user_id: int) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            DELETE FROM BlackList WHERE id = ?""", (user_id,))
            await conn.commit()


async def delete(user_id: int) -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            req = '\n'.join([f"DELETE FROM {table} WHERE id = {user_id};"
                             for table in ('Admins', 'Instructors', 'Students', 'Unverified', 'Users')])
            await cursor.executescript(req)
            await conn.commit()


async def _clear() -> None:
    async with aiosqlite.connect(db) as conn:
        async with conn.cursor() as cursor:
            await cursor.executescript("""
            DELETE FROM Admins;
            DELETE FROM Instructors;
            DELETE FROM Students;
            DELETE FROM Rating;
            DELETE FROM Unverified;
            DELETE FROM Users;
            DELETE FROM BlackList;""")
            await conn.commit()


# db = '../../src/config/data.db'
# import asyncio
# asyncio.run(delete(6568348462))
# asyncio.run(init_db())
# asyncio.run(add_admin(6568348462, '', ''))
# asyncio.run(add_instructor(6568348462, 1, '', '', 1))
# asyncio.run(add_student(6568348462, 1, '', '', 1))
# asyncio.run(add_user(6568348462, '', '', 2, 1))
# TODO