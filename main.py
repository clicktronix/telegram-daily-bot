#!/usr/bin/env python
"""The main entry point to the project."""

import logging
from os import getenv
from random import choice
from telebot import TeleBot, types, logger
from dotenv import load_dotenv
from dictionary import task_dictionary

logger.setLevel(logging.DEBUG)
load_dotenv()

token = getenv("token", "TOKEN")
bot = TeleBot(token)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    """Method sends welcome message to user"""
    keyboard = get_inline_task_keyboard()
    bot.send_message(
        message.chat.id,
        "Hello, I will send simple daily tasks for you",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """Handle callbacks with 'get-task' and 'done' data"""
    if call.data == "get-task":
        get_task(call.message)
    elif call.data == "done":
        task_done(call.message)
    else:
        return


def get_task(message):
    """Sends a message with the task to user"""
    task = str(choice(task_dictionary))
    keyboard = types.InlineKeyboardMarkup()
    done_button = types.InlineKeyboardButton(text="Done", callback_data="done")
    get_task_button = types.InlineKeyboardButton(
        text="Get task", callback_data="get-task"
    )
    keyboard.add(done_button, get_task_button)
    bot.send_message(message.chat.id, text=task, reply_markup=keyboard)


def task_done(message):
    """Sends a complete task message to user"""
    keyboard = get_inline_task_keyboard()
    bot.send_message(
        message.chat.id, "You are awesome", reply_markup=keyboard,
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
