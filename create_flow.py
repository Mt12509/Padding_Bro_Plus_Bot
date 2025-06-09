from bot_instance import bot

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Stati utente temporanei
user_states = {}

TIPI = ["Tipo1", "Tipo2", "Tipo3"]
DIMENSIONI = ["Small", "Medium", "Large", "Extra Large"]

@bot.message_handler(commands=["create"])
def start_create(message):
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
    bot.send_message(chat_id, "Seleziona i tipi (puoi deselezionarne massimo 2):", reply_markup=kb)

def send_dimensioni_selection(chat_id, selected):
    kb = InlineKeyboardMarkup()
    for d in DIMENSIONI:
        text = f"✅ {d}" if d in selected else f"❌ {d}"
        kb.add(InlineKeyboardButton(text, callback_data=f"dim_{d}"))
    kb.add(InlineKeyboardButton("Conferma", callback_data="dim_done"))
    bot.send_message(chat_id, "Seleziona le dimensioni (puoi deselezionarne massimo 3):", reply_markup=kb)

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
            f"Hai selezionato:\n"
            f"Tipi: {', '.join(state['tipi'])}\n"
            f"Dimensioni: {', '.join(state['dimensioni'])}"
        )
        bot.send_message(call.message.chat.id, report)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        user_states.pop(call.from_user.id, None)
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