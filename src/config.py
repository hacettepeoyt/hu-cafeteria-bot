# Telegram Bot Token
TELEGRAM_API_KEY: str = ''

# Image Channel ID
IMAGE_CHANNEL_ID: int = 0
TEXT_CHANNEL_ID: int = 0
LOGGER_CHAT_ID: int = 0

# Time Configurations for menu sharing task
SHARE_TIME_HOUR: int = 0
SHARE_TIME_MINUTE: int = 0
UPDATE_DB_TIME_HOUR: int = 0
UPDATE_DB_TIME_MINUTE: int = 0

# Polling or Webhook?
WEBHOOK_CONNECTED: bool = False
PORT: str = ''
WEBHOOK_URL: str = '' + TELEGRAM_API_KEY

# Background Colors (list of Hex Numbers that represents colors)
BACKGROUND_COLORS: list[str] = []
