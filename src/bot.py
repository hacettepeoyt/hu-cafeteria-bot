import html
import json
import logging
import traceback
from datetime import datetime, time, timedelta

import pytz
import telegram.constants
from aiohttp import ClientConnectorError
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from .config import (
    DB,
    TELEGRAM_API_KEY,
    IMAGE_CHANNEL_ID,
    TEXT_CHANNEL_ID,
    LOGGER_CHAT_ID,
    SHARE_TIME_HOUR,
    SHARE_TIME_MINUTE,
    UPDATE_DB_TIME_HOUR,
    UPDATE_DB_TIME_MINUTE,
    WEBHOOK_CONNECTED,
    PORT,
    WEBHOOK_URL)
from .image import generate_image
from .scraper import scrape

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger()

# Utils
tz = pytz.timezone("Europe/Istanbul")


def get_menu(date: str) -> dict:
    with open(DB, 'r') as file:
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
    image_buffer = generate_image(today_date, menu['meals'], menu['calorie'])
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_buffer)


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
        image_buffer = generate_image(custom_date, menu['meals'], menu['calorie'])
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_buffer)
    except KeyError:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Söylediğin tarihe ait bir menü yok maalesef!")


async def send_tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tomorrow_date = (datetime.now(pytz.timezone("Europe/Istanbul")) + timedelta(1)).strftime("%d.%m.%Y")
    menu = get_menu(tomorrow_date)
    image_buffer = generate_image(tomorrow_date, menu['meals'], menu['calorie'])
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_buffer)


# Error Handler
async def err_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Log the error and send a telegram message to notify the developer.

    Below code belongs to python-telegram-bot examples, furkansimsekli "fixed" the 4096 character limit.
    Url: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/errorhandlerbot.py
    """

    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)
    tb_msg = f"{html.escape(tb_string)}"

    # Build the message with some markup and additional information about what happened.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    ctx_msg = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
    )
    await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=ctx_msg, parse_mode=telegram.constants.ParseMode.HTML)

    if len(tb_msg) > 4096:
        tb_msg_list = tb_msg.split("The above exception was the direct cause of the following exception:")

        for tb_msg in tb_msg_list:
            if len(tb_msg) > 4096:
                await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=f"Traceback is too long!",
                                               parse_mode=telegram.constants.ParseMode.HTML)
            else:
                await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=f"<pre>{tb_msg}</pre>",
                                               parse_mode=telegram.constants.ParseMode.HTML)
    else:
        await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=f"<pre>{tb_msg}</pre>",
                                       parse_mode=telegram.constants.ParseMode.HTML)


# Jobs
async def update_db(context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        all_menus = await scrape()

        with open(DB, 'w', encoding="utf-8") as file:
            json.dump(all_menus, file, ensure_ascii=False)
            logger.info("Database has been updated!")
    except ClientConnectorError:
        message = f"Connection Error, can't reach to SKSDB"
        logger.exception(message)
        await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=message)
        context.application.job_queue.run_once(update_db, 3600)
    except:
        message = f"Undefined Error while connecting to the SKSDB"
        logger.exception(message)
        await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=f"{message}\n\n{traceback.format_exc()}")


async def publish_menu_image(context: ContextTypes.DEFAULT_TYPE) -> None:
    today_date = datetime.now().strftime("%d.%m.%Y")
    menu = get_menu(today_date)
    image_buffer = generate_image(today_date, menu['meals'], menu['calorie'])
    await context.bot.send_photo(chat_id=IMAGE_CHANNEL_ID, photo=image_buffer)
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

    app.job_queue.run_once(update_db, 3)
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
