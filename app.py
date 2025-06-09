from dotenv import load_dotenv
from bot_instance import bot
import create_flow
# ... resto del codice ...

load_dotenv()

import os
import flask
import telebot


app = flask.Flask(__name__)

bot = telebot.TeleBot(os.environ["BOT_TOKEN"], threaded=False)

""" Just a simple check if the app is running """

@app.route("/")
def hello():
    return {"status": "ok"}

# Process webhook calls
@app.route("/webhook", methods=["POST"])
def webhook():
    if flask.request.headers.get("content-type") == "application/json":
        json_string = flask.request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ""
    else:
        flask.abort(403)

# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Benvenuto! Questo è un bot demo. Usa /help o /start per vedere questo messaggio."
    )

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://padding-bro-plus-bot.vercel.app/webhook")
