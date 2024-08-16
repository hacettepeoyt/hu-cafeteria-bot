import json
import os

from . import bot
from .config import DB

if __name__ == '__main__':
    # Initialize database file if not exists with an empty dictionary
    if not os.path.exists(DB):
        with open(DB, "w") as file:
            json.dump({}, file)

    bot.main()
