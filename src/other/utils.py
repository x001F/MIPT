from datetime import datetime as dt
from random import choice
import re
import os


def make_link(length: int = 12) -> (str, dt):
    return ''.join(choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                   for _ in range(length)), dt.now()


def escape_md(string: str) -> str:
    return re.sub(pattern=r"([_*\[\]()~`>#+\-=|{}.!\\])", repl=r"\\\1", string=string)


def init_log() -> None:
    if not os.path.exists('src/logs/logfile'):
        with open('src/logs/logfile', 'w') as f:
            f.write('')
