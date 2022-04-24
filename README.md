# Hacettepe Yemekhanecisi
Hacettepe Yemekhanecisi is a Telegram bot that shares the Hacettepe Cafeteria menu on Telegram daily.

## Reminder
Older versions were built with polling method. I decided to run the bot in servers, so switching to webhook\
was a better idea. Here is a good explanation of [polling vs webhook](https://dzone.com/articles/evaluating-webhooks-vs-polling)

## Usage
You can join the Telegram channel from [here](https://t.me/hacettepeyemekhane)\
You can't use it on your own channel, yet. Take a look at "**in the future**" section.

Required libraries and modules are specified in the *requirements.txt*

**config.py** includes **API_KEY** which provided by Telegram, also chat ID etc.
You can find your own chat IDs with **@getidsbot**

This bot currently running under Heroku servers. Procfile is necessary due that.

## Contributing
Pull requests are welcome!
