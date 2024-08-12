from datetime import datetime as dt
from random import randint, choice
from db import add_user, edit_rating
from asyncio import run


async def users():
    _letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    now = dt.now().timestamp()
    for uid in range(2, 7):
        name = ''.join(choice(_letters + ' ') for _ in range(15))
        username = '@' + ''.join(choice(_letters) for _ in range(7))
        phone = randint(79000000000, 79999999999)
        timestamp = int(now) - randint(500_000, 900_000)
        h = uid, name, username, phone, timestamp
        print(h)
        await add_user(*h)


async def rating():
    v = []
    for team_id in range(5):
        quark_count = randint(1, 100)
        print(team_id, ' - ', quark_count)
        v.append((team_id, quark_count))
    await edit_rating(v)
