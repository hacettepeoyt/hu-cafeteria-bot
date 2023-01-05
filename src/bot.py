import datetime
import logging
import os

from telegram import Message, Bot, Update, User
from telegram.ext import Updater, CommandHandler, CallbackContext, Dispatcher, JobQueue
import config
import image

from telegram.ext.utils.types import UD, CD, BD
from typing import Any, Callable, Protocol

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger: logging.Logger = logging.getLogger(__name__)


def give_date() -> str:
    today: datetime.date = datetime.date.today()
    day: int = today.day
    year: int = today.year
    month: str = str(today).split('-')[1]

    return f'{day}.{month}.{year}'


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
    user_id: object = user['id']
    todaysDate: str = give_date()

    image.main(todaysDate)
    context.bot.send_photo(chat_id=user_id, photo=open('menu.png', 'rb'))


def send(update: Update, context: CallbackContext[UD, CD, BD]) -> None:
    user: User = update.message.from_user
    user_id: object = user['id']
    context_args_obj = context.args
    if context_args_obj is not None:
        todaysDate: str = context_args_obj[0]

    try:
        image.main(todaysDate)
        context.bot.send_photo(chat_id=user_id, photo=open('menu.png', 'rb'))
    except:
        context.bot.send_message(chat_id=user_id, text="Hata!")


def main() -> None:
    TOKEN: str = config.API_KEY
    PORT: int = int(os.environ.get('PORT', config.PORT))

    """ Updater and Dispatcher inherits from a generic type so this annotation will be blank.
        As Updater uses types from telegram.ext.utils and the used ones are unbound, below annotations are still TODO.
    """
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher # type: ignore[has-type]
    job_queue: JobQueue = updater.job_queue # type: ignore[has-type]

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
