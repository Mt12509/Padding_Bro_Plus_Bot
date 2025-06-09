import random
from bot_instance import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

user_states = {}

TIPI = ["Grasso 🫃🏻", "Muscoli 💪🏻", "Cazzo 🍆"]
DIMENSIONI = ["XL Naturale ▶️", "XL Innaturale ⏩", "Estremo Innaturale ⏭️", "Dettaglio Specifico 🔁"]
DETTAGLI_GRASSO = ["Pancia", "Fatpad", "Gambe", "Braccia", "Schiena", "Fianchi", "Torso Superiore"]
DETTAGLI_MUSCOLI = ["Petto", "Addome", "Quadricipiti", "Polpacci", "V-Shape", "Spalle", "Braccia", "Schiena"]
DETTAGLI_CAZZO = ["Palle", "Lunghezza", "Cazzo", "Fusto", "Cappella", "Larghezza", "Pene Curvo", "Sporgente"]

@bot.message_handler(commands=["create"])
def start_create(message):
    print("Handler /create command chiamato")
    user_states[message.from_user.id] = {
        "tipi": TIPI.copy(),
        "dimensioni": DIMENSIONI.copy(),
        "step": "tipi"
    }
    send_tipi_selection(message.chat.id, user_states[message.from_user.id]["tipi"])

def send_tipi_selection(chat_id, selected):
    kb = InlineKeyboardMarkup()
    for t in TIPI:
        text = f"✅ {t}" if t in selected else f"❌ {t}"
        kb.add(InlineKeyboardButton(text, callback_data=f"tipi_{t}"))
    kb.add(InlineKeyboardButton("Conferma", callback_data="tipi_done"))
    bot.send_message(
    chat_id,
    "*Benvenuto nella creazione del tuo padding con PaddingBro+!* 🧸\n\n"
    "Tra poco ti invierò una serie di messaggi con dei menu: scegli gli interessi che più ti rappresentano (o che ti ispirano oggi 🌀).\n"
    "Una volta finito, mescolerò tutto e creerò per te un *padding completamente casuale*! ✨\n\n"
    "Pronto a vedere cosa ne viene fuori? Let's go! 🚀",
    parse_mode="Markdown"
)
    bot.send_message(chat_id, "💥 Scegli i tipi di padding che ti interessano di più:\\n\\(Quando hai finito, clicca su *Conferma* e lascia che l'algoritmo faccia le sue magie\\ 🪄\\)", reply_markup=kb)

def send_dimensioni_selection(chat_id, selected):
    kb = InlineKeyboardMarkup()
    for d in DIMENSIONI:
        text = f"✅ {d}" if d in selected else f"❌ {d}"
        kb.add(InlineKeyboardButton(text, callback_data=f"dim_{d}"))
    kb.add(InlineKeyboardButton("✔️ Conferma ✔️", callback_data="dim_done"))
    bot.send_message(chat_id, "Seleziona le dimensioni del padding che ti interessano:\n (Scegli Conferma per continuare)", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("tipi_") or call.data == "tipi_done")
def handle_tipi(call):
    state = user_states.get(call.from_user.id)
    if not state or state["step"] != "tipi":
        return
    if call.data == "tipi_done":
        state["step"] = "dimensioni"
        send_dimensioni_selection(call.message.chat.id, state["dimensioni"])
        bot.delete_message(call.message.chat.id, call.message.message_id)
        return
    tipo = call.data.split("_", 1)[1]
    if tipo in state["tipi"]:
        if len(state["tipi"]) > 1:
            state["tipi"].remove(tipo)
    else:
        if len(state["tipi"]) < 3:
            state["tipi"].append(tipo)
    send_tipi_selection(call.message.chat.id, state["tipi"])
    bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("dim_") or call.data == "dim_done")
def handle_dimensioni(call):
    state = user_states.get(call.from_user.id)
    if not state or state["step"] != "dimensioni":
        return
    if call.data == "dim_done":
        state["step"] = "done"
        report = (
            f"🧾 Resoconto selezione:\n"
            f"Tipi: {', '.join(state['tipi'])}\n"
            f"Dimensioni: {', '.join(state['dimensioni'])}"
        )
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("💥 CREA 💥", callback_data="crea_finale"))
        bot.send_message(call.message.chat.id, report, reply_markup=kb)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        return
    dim = call.data.split("_", 1)[1]
    if dim in state["dimensioni"]:
        if len(state["dimensioni"]) > 1:
            state["dimensioni"].remove(dim)
    else:
        if len(state["dimensioni"]) < 4:
            state["dimensioni"].append(dim)
    send_dimensioni_selection(call.message.chat.id, state["dimensioni"])
    bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "crea_finale")
def handle_crea(call):
    state = user_states.get(call.from_user.id)
    if not state or state["step"] != "done":
        return
    tipo = random.choice(state["tipi"])
    dimensione = random.choice(state["dimensioni"])
    dettaglio = None
    if dimensione == "Dettaglio Specifico":
        if tipo == "Grasso":
            dettaglio = random.choice(DETTAGLI_GRASSO)
        elif tipo == "Muscoli":
            dettaglio = random.choice(DETTAGLI_MUSCOLI)
        elif tipo == "Cazzo":
            dettaglio = random.choice(DETTAGLI_CAZZO)
    if dettaglio:
        msg = f"🧾 Risultato casuale:\nTipo: {tipo}\nDimensione: {dimensione}\nDettaglio: {dettaglio}"
    else:
        msg = f"🧾 Risultato casuale:\nTipo: {tipo}\nDimensione: {dimensione}"
    bot.send_message(call.message.chat.id, msg)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    user_states.pop(call.from_user.id, None)

@bot.message_handler(commands=["debug"])
def debug(message):
    user_id = message.from_user.id
    state = user_states.get(user_id, {})
    bot.send_message(
        message.chat.id,
        f"Stato utente {user_id}:\n"
        f"Tipi: {state.get('tipi', [])}\n"
        f"Dimensioni: {state.get('dimensioni', [])}\n"
        f"Step: {state.get('step', 'unknown')}"
    )