import datetime
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import fetchingMenu
import config
import creatingPicture


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hacettepe Yemekhanecisi'ne hoşgeldin Hacettepeli!")


def updateDatabase(context: CallbackContext):
    fetchingMenu.fetch_data_fromXML()
    context.bot.send_message(chat_id=config.admin_id, text="Time to refresh my memory!")


def send_dailyMenu(context: CallbackContext):

    # Reformatting the date to search in database
    todaysDate = str(datetime.date.today()).replace("-", ".")
    if todaysDate[8] == '0':
        todaysDate = todaysDate[:8] + todaysDate[-1]

    # Texts will be printed on background image and then, bot will send it
    creatingPicture.main(todaysDate)
    context.bot.send_photo(chat_id=config.chat_id, photo=open('menu.png', 'rb'))


def send_now(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user['id']
    todaysDate = str(context.args[0])

    # Texts will be printed on background image and then, bot will send it
    creatingPicture.main(todaysDate)
    context.bot.send_photo(chat_id=user_id, photo=open('menu.png', 'rb'))


def isOnline(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=config.admin_id, text="Yes father, I'm alive..")


def main():
    TOKEN = config.API_KEY
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start)),
    dispatcher.add_handler(CommandHandler("online_status", isOnline))
    dispatcher.add_handler(CommandHandler("send_now", send_now))

    # job_queue works in UTC time zone, it will be updated in the future versions of the bot!
    # First job is updating menu files every day at midnight
    # Second job is sending the menu to the channel
    updater.job_queue.run_daily(updateDatabase, time=datetime.time(hour=4, minute=55))
    updater.job_queue.run_daily(send_dailyMenu, time=datetime.time(hour=5, minute=0))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='https://infinite-wildwood-55276.herokuapp.com/' + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
