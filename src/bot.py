import datetime
import logging
import os

from telegram import Update, User
from telegram.ext import Updater, CommandHandler, CallbackContext

import config
import image


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger: logging.Logger = logging.getLogger(__name__)


def give_date() -> str:
    today = datetime.date.today()
    day, year = today.day, today.year
    month = str(today).split('-')[1]

    return f'{day}.{month}.{year}'


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "@hacettepeyemekhane kanalından düzenli olarak menülere ulaşabilirsin!")


def send_dailyMenu(context: CallbackContext):
    todaysDate: str = give_date()

    image.main(todaysDate)
    context.bot.send_photo(chat_id=config.CHANNEL_ID,
                           photo=open('menu.png', 'rb'))


def send_now(update: Update, context: CallbackContext):
    user: User = update.message.from_user
    user_id: object = user['id']
    todaysDate: str = give_date()

    image.main(todaysDate)
    context.bot.send_photo(chat_id=user_id, photo=open('menu.png', 'rb'))


def send(update: Update, context: CallbackContext):
    user: User = update.message.from_user
    user_id: object = user['id']
    todaysDate: str = context.args[0]

    try:
        image.main(todaysDate)
        context.bot.send_photo(chat_id=user_id, photo=open('menu.png', 'rb'))
    except:
        context.bot.send_message(chat_id=user_id, text="Hata!")


def main():
    TOKEN = config.API_KEY
    PORT = int(os.environ.get('PORT', config.PORT))
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start)),
    dispatcher.add_handler(CommandHandler("send_now", send_now))
    dispatcher.add_handler(CommandHandler("send", send))

    updater.job_queue.run_daily(send_dailyMenu, time=datetime.time(
        hour=config.SHARE_TIME_HOUR, minute=config.SHARE_TIME_MINUTE))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=config.WEBHOOK_URL)
    updater.idle()


if __name__ == '__main__':
    main()
