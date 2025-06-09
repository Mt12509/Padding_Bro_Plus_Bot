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
    "🛠 *Comandi disponibili su PaddingBro+*\n"
        "Hai il potere del padding tra le mani. Ecco come usarlo al meglio 👇\n\n"
        "• /start - Mostra il messaggio di benvenuto e panoramica del bot ⏯️\n"
        "• /create - Avvia la creazione guidata di un padding casuale _(con scelta di tipo e dimensione)_ 🤖\n"
        "• /app - Scopri l'app ufficiale con funzionalità extra e l'esclusiva *modalità SnappThicc* 💾\n"
        "• /help - Stai guardando proprio questo! Ti mostra tutti i comandi disponibili 🔍\n"
        "• /about - Scopri di più su PaddingBro+ e il suo creatore 🦸🏻‍♂️\n\n"
        "✨ Altre funzioni stanno arrivando. Resta connesso e continua a creare padding leggendari.\n\n"
        "_PaddingBro+ ti guarda. 👀_", parse_mode="Markdown")

@bot.message_handler(commands=["about"])
def send_about(message):
    bot.reply_to(
        message,
        "*PaddingBro+* è stato creato con 💚 da [@Mt12509](https://t.me/Mt12509)!\n\n"
    "🚀 L'app ufficiale _(con funzioni esclusive tipo *SnappThicc*)_ e il codice del bot sono open source su GitHub:\n"
    "[github.com/Mt12509/Padding_Bro_Plus](https://github.com/Mt12509/)\n\n"
    "💡 Hai un'idea per migliorare il bot? Vuoi suggerire funzioni, modifiche o nuove idee?\n"
    "Scrivimi su Telegram o apri una issue su GitHub!\n\n"
    "☕ Ti piace il progetto e vuoi supportarlo?\n"
    "Puoi lasciare una birretta o un caffè virtuale qui:\n"
    "[Coming Soon!](https://google.com)\n\n"
    "_Ogni tip, stella o consiglio è super apprezzato!_\n\n"
    "*Grazie per usare PaddingBro+.\n Il padding non sarà mai più lo stesso.* 💥",
        parse_mode="Markdown", disable_web_page_preview=True
    )


@bot.message_handler(func=lambda message: message.text and message.text.startswith("/"))
def unknown_command(message):
    bot.reply_to(
        message,
        "❌ *Comando non riconosciuto, bro.* 😅\n"
    "Forse hai scritto male o hai scoperto un padding segreto! 🕵️‍♂️\n\n"
    "Digita /help per vedere tutti i comandi disponibili e tornare a dominare il padding. 💪",
        parse_mode="Markdown"
    )
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://padding-bro-plus-bot.vercel.app/webhook")
