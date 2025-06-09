import create_flow
from dotenv import load_dotenv
load_dotenv()

from bot_instance import bot


import os
import flask
import telebot


app = flask.Flask(__name__)


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
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message,
    "👋 *Benvenuto su PaddingBro+!*\nIl bot che porta il padding a livelli mai visti 😎\n\n"
    "Con questo bot puoi:\n"
    "• 🎲 *Creare padding casuali* basati sui tuoi gusti\n"
    "• 📏 *Scegliere tipo e dimensione* con menu interattivi\n"
    "• 💾 *Salvare le tue combo leggendarie* con la funzione esclusiva *SnappThicc* _(solo su app)_\n"
    "• 🚀 *Esplorare nuove combinazioni* ogni volta che vuoi\n\n"
    "ℹ️ Usa il comando /help per vedere tutti i comandi disponibili\n"
    "Oppure prova subito con /create e lascia fare al destino 💥", parse_mode="Markdown")

@bot.message_handler(commands=["help"])
def send_help(message):
    bot.reply_to(message,
    "🛠 *Comandi disponibili su PaddingBro+* \\n"
    "Hai il potere del padding tra le mani\\. Ecco come usarlo al meglio 👇\n\n"
    
    "• /start - Mostra il messaggio di benvenuto e panoramica del bot ⏯️\n"
    "• /create - Avvia la creazione guidata di un padding casuale _(con scelta di tipo e dimensione)_ 🤖\n"
    "• /app - Scopri l'app ufficiale con funzionalità extra e l'esclusiva *modalità SnappThicc* 💾\n"
    "• /help - Stai guardando proprio questo! Ti mostra tutti i comandi disponibili 🔍\n\n"
    "• /about - Scopri di più su PaddingBro+ e il suo creatore 🦸🏻‍♂️\n"
    
    "✨ Altre funzioni stanno arrivando. Resta connesso e continua a creare padding leggendari. \n"
    "_PaddingBro+ ti guarda. 👀", parse_mode="Markdown")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://padding-bro-plus-bot.vercel.app/webhook")
