import datetime
import json
import logging

from telegram import Update, User
from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue
from telegram.ext.utils.types import UD, CD, BD

import image
import scraper
from config import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger: logging.Logger = logging.getLogger()


def get_date() -> str:
    return datetime.datetime.now().strftime("%d.%m.%Y")


def get_menu(date: str) -> dict:
    with open("database.json", 'r') as file:
        menu = json.load(file)[date]
    return menu


def start(update: Update, context: CallbackContext[UD, CD, BD]) -> None:
    update.message.reply_text(text="@hacettepeyemekhane kanalından düzenli olarak menülere ulaşabilirsin!")


def send_now(update: Update, context: CallbackContext[UD, CD, BD]) -> None:
    user: User = update.message.from_user
    today_date: str = get_date()
    menu = get_menu(today_date)
    image.generate_image(today_date, menu['meals'], menu['calorie'])
    context.bot.send_photo(chat_id=user.id, photo=open("menu.png", "rb"))


def send(update: Update, context: CallbackContext[UD, CD, BD]) -> None:
    user: User = update.message.from_user
    today_date: str = context.args[0]

    try:
        menu = get_menu(today_date)
        image.generate_image(today_date, menu['meals'], menu['calorie'])
        context.bot.send_photo(chat_id=user.id, photo=open("menu.png", "rb"))
    except:
        context.bot.send_message(chat_id=user.id, text="Hata!")


def send_daily(context: CallbackContext[UD, CD, BD]) -> None:
    today_date: str = get_date()
    menu = get_menu(today_date)
    image.generate_image(today_date, menu['meals'], menu['calorie'])
    context.bot.send_photo(chat_id=IMAGE_CHANNEL_ID, photo=open("menu.png", "rb"))


def update_db(context: CallbackContext[UD, CD, BD]):
    all_menu = scraper.scrape()
    with open("database.json", 'w', encoding="utf-8") as file:
        json.dump(all_menu, file, ensure_ascii=False, indent=4)


def main() -> None:
    """
    Updater and Dispatcher inherits from a generic type so this annotation will be blank.
    As Updater uses types from telegram.ext.utils and the used ones are unbound, below annotations are still TODO.
    """

    updater = Updater(token=TELEGRAM_API_KEY)
    dispatcher = updater.dispatcher  # type: ignore[has-type]
    job_queue: JobQueue = updater.job_queue  # type: ignore[has-type]
    dispatcher.add_handler(CommandHandler(command="start", callback=start)),
    dispatcher.add_handler(CommandHandler(command="send_now", callback=send_now))
    dispatcher.add_handler(CommandHandler(command="send", callback=send))

    job_queue.run_daily(send_daily, time=datetime.time(hour=SHARE_TIME_HOUR, minute=SHARE_TIME_MINUTE))
    job_queue.run_daily(update_db, time=datetime.time(hour=UPDATE_DB_TIME_HOUR, minute=UPDATE_DB_TIME_MINUTE))

    if WEBHOOK_CONNECTED:
        updater.start_webhook(listen="0.0.0.0",
                              port=int(PORT),
                              url_path=TELEGRAM_API_KEY,
                              webhook_url=WEBHOOK_URL)
    else:
        updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
