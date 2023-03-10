from datetime import datetime, time, timedelta
import html
import json
import logging
import pytz
import traceback

import telegram.constants
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from .config import *
from .image import generate_image
from .scraper import scrape

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger()

# Utils
tz = pytz.timezone("Europe/Istanbul")


def get_menu(date: str) -> dict:
    with open("database.json", 'r') as file:
        menu = json.load(file)[date]
    return menu


def generate_menu_text(menu: dict) -> str:
    message = f"<b>Günün Menüsü</b>\n\n"
    for meal in menu['meals']:
        message += f"- {meal}\n"
    message += f"\nToplam: {menu['calorie']} cal"
    return message


# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Merhaba! Menülerden haberdar olmak için @hacettepeyemekhane kanalına "
                                        "katılmalısın!\n\nYardım için /help komutunu kullanmalısın.")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Aşağıdaki menü butonundan kullanabileceğin komutları öğrenebilirsin.\n\n\n"
                                        "/today   -->   Bugünün menüsünü öğrenmek için kullanabilirsin.\n\n"
                                        "/tomorrow   -->   Yarının menüsünü öğrenmek için kullanabilirsin.\n\n"
                                        "/custom   -->   Farklı bir günün menüsünü öğrenmek için kullanabilirsin.\n"
                                        "<b>Örnek:</b> <i>/custom 01.01.2023</i>",
                                   parse_mode=telegram.constants.ParseMode.HTML)


async def send_today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    today_date = datetime.now(tz).strftime("%d.%m.%Y")
    menu = get_menu(today_date)
    generate_image(today_date, menu['meals'], menu['calorie'])
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("menu.png", "rb"))


async def send_custom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="İstediğin tarihi lütfen belirt!\n"
                                            "<b>Örnek:</b> <i>/custom 01.01.2023</i>",
                                       parse_mode=telegram.constants.ParseMode.HTML)
        return

    try:
        custom_date = context.args[0]
        menu = get_menu(custom_date)
        generate_image(custom_date, menu['meals'], menu['calorie'])
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("menu.png", "rb"))
    except KeyError:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Söylediğin tarihe ait bir menü yok maalesef!")


async def send_tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    today_date = (datetime.now(pytz.timezone("Europe/Istanbul")) + timedelta(1)).strftime("%d.%m.%Y")
    menu = get_menu(today_date)
    generate_image(today_date, menu['meals'], menu['calorie'])
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("menu.png", "rb"))


# Error Handler
async def err_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Below code belongs to python-telegram-bot examples.
    Url: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/errorhandlerbot.py
    """
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096-character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=message, parse_mode=telegram.constants.ParseMode.HTML)


# Jobs
async def update_db(context: ContextTypes.DEFAULT_TYPE) -> None:
    all_menus = await scrape()
    with open("database.json", 'w', encoding="utf-8") as file:
        json.dump(all_menus, file, ensure_ascii=False, indent=4)
    logger.info("Database has been updated!")


async def publish_menu_image(context: ContextTypes.DEFAULT_TYPE) -> None:
    today_date = datetime.now().strftime("%d.%m.%Y")
    menu = get_menu(today_date)
    generate_image(today_date, menu['meals'], menu['calorie'])
    await context.bot.send_photo(chat_id=IMAGE_CHANNEL_ID, photo=open("menu.png", "rb"))
    logger.info("Image has been sent to channel")


async def publish_menu_text(context: ContextTypes.DEFAULT_TYPE) -> None:
    today_date = datetime.now().strftime("%d.%m.%Y")
    menu = get_menu(today_date)
    message = generate_menu_text(menu)
    await context.bot.send_message(chat_id=TEXT_CHANNEL_ID, text=message, parse_mode=telegram.constants.ParseMode.HTML)
    logger.info("Text has been sent to channel")


def main() -> None:
    
    app: Application = Application.builder().token(TELEGRAM_API_KEY).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("today", send_today))
    app.add_handler(CommandHandler("tomorrow", send_tomorrow))
    app.add_handler(CommandHandler("custom", send_custom))
    app.add_error_handler(err_handler)
    app.job_queue.run_once(update_db, 3) #Updates db when program starts
    app.job_queue.run_daily(update_db, time=time(hour=UPDATE_DB_TIME_HOUR, minute=UPDATE_DB_TIME_MINUTE, tzinfo=tz))
    app.job_queue.run_daily(publish_menu_image, time=time(hour=SHARE_TIME_HOUR, minute=SHARE_TIME_MINUTE, tzinfo=tz))
    app.job_queue.run_daily(publish_menu_text, time=time(hour=SHARE_TIME_HOUR, minute=SHARE_TIME_MINUTE, tzinfo=tz))

    if WEBHOOK_CONNECTED:
        app.run_webhook(listen="0.0.0.0",
                        port=int(PORT),
                        url_path=TELEGRAM_API_KEY,
                        webhook_url=WEBHOOK_URL)
    else:
        app.run_polling()


if __name__ == "__main__":
    main()
