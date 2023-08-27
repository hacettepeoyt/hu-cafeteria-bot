import sys

import toml

config_path = sys.argv[1] if len(sys.argv) > 1 else "config.toml"
config = toml.load(config_path)

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
