import datetime
import logging
import os
import json

from telegram import Message, Bot, Update, User
from telegram.ext import Updater, CommandHandler, CallbackContext, Dispatcher, JobQueue
import config
import image

from telegram.ext.utils.types import UD, CD, BD
from typing import Any, Callable, Protocol
from scraper import fetch_data_fromXML
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger: logging.Logger = logging.getLogger(__name__)


def give_date() -> str:
    return datetime.datetime.now().strftime("%d.%m.%Y")


def start(update: Update, context: CallbackContext[UD, CD, BD]) -> None:
    update.message.reply_text(
        text="@hacettepeyemekhane kanalından düzenli olarak menülere ulaşabilirsin!")


def send_dailyMenu(context: CallbackContext[UD, CD, BD]) -> None:
    todaysDate: str = give_date()

    image.main(todaysDate)
    context.bot.send_photo(chat_id=config.CHANNEL_ID,
                           photo=open('menu.png', 'rb'))


def send_now(update: Update, context: CallbackContext[UD, CD, BD]) -> None:
    user: User = update.message.from_user
    todaysDate: str = give_date()

    image.main(todaysDate)
    context.bot.send_photo(chat_id=user.id, photo=open('menu.png', 'rb'))


def send(update: Update, context: CallbackContext[UD, CD, BD]) -> None:
    user: User = update.message.from_user
    context_args_obj = context.args
    if context_args_obj is not None:
        todaysDate: str = context_args_obj[0]

    try:
        image.main(todaysDate)
        context.bot.send_photo(chat_id=user.id, photo=open('menu.png', 'rb'))
    except:
        context.bot.send_message(chat_id=user.id, text="Hata!")

def update_db(context: CallbackContext[UD, CD, BD]) :
    print(fetch_data_fromXML())
    # Update the database here
    with open("JSON_Database.json", "r", encoding="utf-8") as file:
        database = json.load(file)
    today_menu = database[give_date()]
    today_meals = today_menu["meals"]
    today_calorie = today_menu["kalori"]

    return today_meals, today_calorie


def main() -> None:
    TOKEN: str = config.API_KEY
    print(config.PORT)
    PORT: int = int(os.environ.get('PORT', config.PORT))

    """ Updater and Dispatcher inherits from a generic type so this annotation will be blank.
        As Updater uses types from telegram.ext.utils and the used ones are unbound, below annotations are still TODO.
    """
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher # type: ignore[has-type]
    job_queue: JobQueue = updater.job_queue # type: ignore[has-type]
    job_queue.run_daily(update_db, time=datetime.time(hour=15, minute=0))
    dispatcher.add_handler(CommandHandler(command="start", callback=start)),
    dispatcher.add_handler(CommandHandler(
        command="send_now", callback=send_now))
    dispatcher.add_handler(CommandHandler(command="send", callback=send))

    job_queue.run_daily(send_dailyMenu, time=datetime.time(
        hour=config.SHARE_TIME_HOUR, minute=config.SHARE_TIME_MINUTE))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=config.WEBHOOK_URL)
    updater.idle()


if __name__ == '__main__':
    main()