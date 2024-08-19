# mipt
MIPT - final project on 3rd week of the summer school, telegram bot

## Requirements
 - [Python 3](https://www.python.org/downloads/release/python-3120/)
 - [aiogram](https://aiogram.dev)
 - [aiosqlite](https://pypi.org/project/aiosqlite/)

## Usage
First clone this repository, then install required libraries running the command
```sh
pip3 install -r requirements.txt
```

Then insert token given by the [BotFather](https://t.me/botfather) into [config.py](src/config/config.py) "BOT_TOKEN" variable
After that you have to fill [config.py](src/config/config.py) with required info like contacts, phone numbers, etc.
And finally run [main.py](main.py) to run the bot.
```sh
python3 main.py
```

## Logging
This bot uses built-in module (logging)
logging config is in [config.py](src/config/config.py)
