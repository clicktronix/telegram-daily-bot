from os import getenv
from telebot import TeleBot, types, logger
from dotenv import load_dotenv
from dictionary import task_dictionary
from random import choice
import logging

logger.setLevel(logging.DEBUG)
load_dotenv()

token = getenv("token", "TOKEN")
bot = TeleBot(token)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup()
    send_task_button = types.InlineKeyboardButton(
        text="Get task", callback_data="get-task"
    )
    keyboard.add(send_task_button)
    bot.send_message(
        message.chat.id,
        "Hello, I will send simple daily tasks for you",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "get-task":
        get_task(call.message)
    elif call.data == "done":
        task_done(call.message)
    else:
        return


def get_task(message):
    task = str(choice(task_dictionary))
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Done", callback_data="done")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, text=task, reply_markup=keyboard)


def task_done(message):
    bot.send_message(message.chat.id, "You are awesome")


if __name__ == "__main__":
    bot.polling()
