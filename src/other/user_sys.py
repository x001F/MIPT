from src.other import delete_user, get_recent_users
from datetime import datetime as dt


async def filter_recently_users():
    now_ts = dt.now().timestamp()
    users_to_delete = filter(lambda user: now_ts - user[4] >= 604800, await get_recent_users())
    for i_user in users_to_delete:
        await delete_user(i_user[0])
