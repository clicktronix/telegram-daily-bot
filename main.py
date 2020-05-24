#!/usr/bin/env python
"""The main entry point to the project."""

import logging
import random
from telebot import TeleBot, types, logger
from dotenv import load_dotenv
from config import Config
from db import Database

logger.setLevel(logging.DEBUG)
load_dotenv()
bot = TeleBot(Config.TOKEN)
database = Database(Config)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    """Method sends welcome message to user"""
    database.connect()
    keyboard = get_inline_task_keyboard()
    bot.send_message(
        message.chat.id,
        "Hello, I will send simple daily tasks for you",
        reply_markup=keyboard,
    )
    database.update_rows(
        "INSERT INTO chat (id) VALUES (%s) ON CONFLICT (id) DO NOTHING;",
        [message.chat.id],
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """Handle callbacks with 'get-task' and 'done' data"""
    if call.data == "get-task":
        get_task(call.message.chat.id)
    elif call.data == "done":
        task_done(call.message.chat.id)
    else:
        return


def get_task(chat_id):
    """Sends a message with the task to user"""
    tasks = database.select_rows("SELECT * FROM tasks;")
    task = random.choice(tasks)

    keyboard = types.InlineKeyboardMarkup()
    done_button = types.InlineKeyboardButton(text="Done", callback_data="done")
    get_task_button = types.InlineKeyboardButton(
        text="Get task", callback_data="get-task"
    )
    keyboard.add(done_button, get_task_button)
    bot.send_message(chat_id, text=task.task, reply_markup=keyboard)


def task_done(chat_id):
    """Sends a complete task message to user"""
    keyboard = get_inline_task_keyboard()
    bot.send_message(
        chat_id, "You are awesome", reply_markup=keyboard,
    )


def get_inline_task_keyboard():
    """Returns inline keyboard"""
    keyboard = types.InlineKeyboardMarkup()
    get_task_button = types.InlineKeyboardButton(
        text="Get task", callback_data="get-task"
    )
    keyboard.add(get_task_button)
    return keyboard


if __name__ == "__main__":
    bot.polling()
