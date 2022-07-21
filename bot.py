from requests import get
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import random
import os
from base64 import decodebytes

TOKEN = os.environ.get("TOKEN")
PORT = os.environ.get("PORT", 5000)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

topics = ['gk', 'books', 'film', 'music', 'theaters', 'television', 'video_games', 'board_games', 'science_and_nature',
          'computers', 'maths', 'mythology', 'sports', 'geography', 'history', 'politics', 'art', 'celebrities',
          'animals', 'vehicles', 'comics', 'science_gadgets', 'japanese_anims', 'cartoon_animations']


def start(update, context):
    message = "Hi {} !! ,This bot is developed by @TheShubhendra\nEnjoy with the bot.".format(
        update.message.from_user.first_name)
    context.bot.send_message(update.message.chat_id, message)


def fetch(update, context):
    print(update.message.chat_id)
    cat = random.randint(9, len(topics) + 8)
    text = update.message.text
    for x in topics:
        if x in text:
            cat = topics.index(x) + 9

    diff = ["easy", "medium", "hard"]
    url = "https://opentdb.com/api.php?amount=1&category={}&difficulty={}&type=multiple&encode=base64".format(cat, diff[
        random.randint(0, 2)])
    print(url)
    resp = get(url).json()
    res = resp["results"][0]

    q = decodebytes(res["question"].encode()).decode()
    print(q)
    options = res["incorrect_answers"]
    ans = res["correct_answer"]
    i = random.randint(0, 3)
    options.insert(i, ans)
    options = [decodebytes(x.encode()).decode() for x in options]
    context.bot.send_poll(chat_id=update.message.chat_id, question=q, options=options, type="quiz", is_anonymous=False,
                          correct_option_id=i)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

handler = CommandHandler(topics + ["random"], fetch)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(handler)
dispatcher.add_handler(start_handler)
if WEBHOOK_URL is not None:
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook(WEBHOOK_URL + TOKEN)
else:
    updater.start_polling()
updater.idle()
