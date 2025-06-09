# bot_instance.py
import telebot
import os

bot = telebot.TeleBot(os.environ["BOT_TOKEN"], threaded=False)