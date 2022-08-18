import datetime
import logging
import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import config
import image


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def give_date():
    today = datetime.date.today()
    day, year = today.day, today.year
    month = str(today).split('-')[1]               # Thanks to this way, we are able to do take month value as not integer. We want values like 09 (not 9)

    return f'{day}.{month}.{year}'


def start(update: Update, context: CallbackContext):
    update.message.reply_text("@hacettepeyemekhane kanalından düzenli olarak menülere ulaşabilirsin!")


def send_dailyMenu(context: CallbackContext):
    todaysDate = give_date()

    image.main(todaysDate)
    context.bot.send_photo(chat_id=config.chat_id, photo=open('menu.png', 'rb'))


def send_now(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user['id']
    todaysDate = give_date()

    image.main(todaysDate)
    context.bot.send_photo(chat_id=user_id, photo=open('menu.png', 'rb'))


def send(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user['id']
    todaysDate = context.args[0]

    try:
        image.main(todaysDate)
        context.bot.send_photo(chat_id=user_id, photo=open('menu.png', 'rb'))
    except:
        context.bot.send_message(chat_id=user_id, text="Hata!")


def main():
    TOKEN = config.API_KEY
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start)),
    dispatcher.add_handler(CommandHandler("send_now", send_now))
    dispatcher.add_handler(CommandHandler("send", send))

    updater.job_queue.run_daily(send_dailyMenu, time=datetime.time(hour=6, minute=15))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='https://infinite-wildwood-55276.herokuapp.com/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
