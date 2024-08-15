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
DB = args.database

# Telegram Bot Token
TELEGRAM_API_KEY: str = config["TELEGRAM_API_KEY"]

# Image Channel ID
IMAGE_CHANNEL_ID: int = config["IMAGE_CHANNEL_ID"]
TEXT_CHANNEL_ID: int = config["TEXT_CHANNEL_ID"]
LOGGER_CHAT_ID: int = config["LOGGER_CHAT_ID"]

# Time Configurations for menu sharing task
SHARE_TIME_HOUR: int = config.get("SHARE_TIME_HOUR", 9)
SHARE_TIME_MINUTE: int = config.get("SHARE_TIME_MINUTE", 15)
UPDATE_DB_TIME_HOUR: int = config.get("UPDATE_DB_TIME_HOUR", 15)
UPDATE_DB_TIME_MINUTE: int = config.get("UPDATE_DB_TIME_MINUTE", 0)

# Polling or Webhook?
WEBHOOK_CONNECTED: bool = config.get("WEBHOOK_CONNECTED", False)
PORT: int = config.get("PORT", 51413)
WEBHOOK_URL: str = config.get("WEBHOOK_URL", "") + "/" + TELEGRAM_API_KEY

# Background Colors (list of Hex Numbers that represents colors)
BACKGROUND_COLORS: list[str] = config.get("BACKGROUND_COLORS", ["#C9D6DF", "#F8F3D4", "#FFE2E2", "#E7D4B5", "#AEDEFC",
                                                                "#EAFFD0", "#FFD3B4", "#BAC7A7", "#95E1D3", "#FCE38A",
                                                                "#FFB4B4"])

# Email Configuration
SMTP_HOST = config["SMTP_HOST"]
SMTP_PORT = config.get("SMTP_PORT", 587)
SMTP_USERNAME = config["SMTP_USERNAME"]
SMTP_PASSWORD = config["SMTP_PASSWORD"]
MAILING_LIST_ADDRESS = config["MAILING_LIST_ADDRESS"]
