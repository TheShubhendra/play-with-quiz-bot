from requests import get
from telegram.ext import Updater , CommandHandler, MessageHandler, Filters
import logging
import random
from base64 import decodebytes
TOKEN = os.environ.get("TOKEN")
PORT = os.environ.get("PORT",5000)
def start(update,context):
    message = "Hi {} !! , Enjoy with the bot.".format(update.message.from_user.first_name)
    context.bot.send_message(update.message.chat_id,message)
  
def fetch(update,context):
  
  
  text= update.message.text
  if "science" in text:
    cat  ="17"
  if "computer" in text:
    cat = "18"
  elif "maths" in text:
    cat = "19"
  elif "history" in text:
    cat = "23"
  diff=["easy","medium","hard"]
  url ="https://opentdb.com/api.php?amount=1&category={}&difficulty={}&type=multiple&encode=base64".format(cat,diff[random.randint(0,2)])
  print(url)
  resp = get(url).json()
  res = resp["results"][0]
  

  q = decodebytes(res["question"].encode()).decode()
  print(q)
  options = res["incorrect_answers"]
  ans = res["correct_answer"]
  i = random.randint(0,3)
  options.insert(i,ans)
  print(*options)
  options = [decodebytes(x.encode()).decode() for x in options]
  context.bot.send_poll(chat_id=update.message.chat_id, question=q,options=options,type="quiz",is_anonymous=True,correct_option_id=i)
    
  
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(TOKEN,use_context=True)
dispatcher = updater.dispatcher

handler = CommandHandler(["science","computer","history","maths"],fetch)
start_handler = CommandHandler('start',start)
dispatcher.add_handler(handler)
dispatcher.add_handler(start_handler)

updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
updater.bot.setWebhook("https://play-with-quiz-bot.herokuapp.com/" + TOKEN)

updater.idle()
