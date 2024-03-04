import argparse
from pathlib import Path

import toml

parser = argparse.ArgumentParser(description='A Telegram Bot to let people know about Hacettepe Cafeteria Menus')
parser.add_argument('-c', '--config',
                    type=Path,
                    help='Path to config file written in toml format',
                    required=True)
parser.add_argument('-d', '--database',
                    type=Path,
                    help='Path to database file, written in json format',
                    required=True)

args = parser.parse_args()

config = toml.load(args.config)
db = args.database

# Telegram Bot Token
TELEGRAM_API_KEY: str = config["TELEGRAM_API_KEY"]

# Image Channel ID
IMAGE_CHANNEL_ID: int = config["IMAGE_CHANNEL_ID"]
TEXT_CHANNEL_ID: int = config["TEXT_CHANNEL_ID"]
LOGGER_CHAT_ID: int = config["LOGGER_CHAT_ID"]

# Time Configurations for menu sharing task
SHARE_TIME_HOUR: int = config["SHARE_TIME_HOUR"]
SHARE_TIME_MINUTE: int = config["SHARE_TIME_MINUTE"]
UPDATE_DB_TIME_HOUR: int = config["UPDATE_DB_TIME_HOUR"]
UPDATE_DB_TIME_MINUTE: int = config["UPDATE_DB_TIME_MINUTE"]

# Polling or Webhook?
WEBHOOK_CONNECTED: bool = config["WEBHOOK_CONNECTED"]
PORT: int = config["PORT"]
WEBHOOK_URL: str = config["WEBHOOK_URL"]

# Background Colors (list of Hex Numbers that represents colors)
BACKGROUND_COLORS: list[str] = config["BACKGROUND_COLORS"]
