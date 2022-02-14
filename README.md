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

## In the future

>Using mongodb instead of txt files

>Bot will work in any channel and private chat

>Update: I've found a better way to fetch the data. Probably, I'll use it in the future.

>There will be more background image. Variety is needed :)

>P̶h̶o̶t̶o̶ ̶b̶a̶s̶e̶d̶ ̶m̶e̶s̶s̶a̶g̶e̶s̶ ̶w̶i̶l̶l̶ ̶b̶e̶ ̶u̶s̶e̶d̶ ̶i̶n̶s̶t̶e̶a̶d̶ ̶o̶f̶ ̶j̶u̶s̶t̶ ̶t̶e̶x̶t̶s̶

