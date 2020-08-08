#!/usr/bin/env python
"""The main entry point to the project"""

import logging
import random
from telebot import TeleBot, types, logger
from config import Config
from task_manager import TaskManager

logger.setLevel(logging.DEBUG)
bot = TeleBot(Config.TOKEN)
taskManager = TaskManager()


@bot.message_handler(commands=["start"])
def send_welcome(message):
    """Method sends welcome message to user"""
    keyboard = get_inline_task_keyboard()
    bot.send_message(
        message.chat.id,
        "Hello, I will send simple daily tasks for you",
        reply_markup=keyboard,
    )
    taskManager.insert_chat(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """Handle callbacks with 'get-task' and 'done' data"""
    if call.data == "get-task":
        send_task(call.message.chat.id)
    elif call.data == "done":
        task_done(call.message.chat.id)
    else:
        return


def send_task(chat_id):
    """Sends a message with the task to user"""
    tasks = taskManager.get_tasks(chat_id)
    task_id, task = random.choice(tasks)
    taskManager.insert_done_id(task_id)
    keyboard = types.InlineKeyboardMarkup()
    done_button = types.InlineKeyboardButton(text="Done", callback_data="done")
    get_task_button = types.InlineKeyboardButton(
        text="Get task", callback_data="get-task"
    )
    keyboard.add(done_button, get_task_button)
    bot.send_message(chat_id, text=task, reply_markup=keyboard)


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
