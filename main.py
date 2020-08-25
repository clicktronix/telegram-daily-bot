#!/usr/bin/env python
"""The main entry point to the project"""

import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from config import Config
from task_manager import TaskManager

logging.basicConfig(level=logging.INFO)
bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot)
taskManager = TaskManager()


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    """Method sends welcome message to user"""
    keyboard = get_inline_task_keyboard()
    await bot.send_message(
        message.chat.id,
        "Hello, I will send simple daily tasks for you",
        reply_markup=keyboard,
    )
    taskManager.insert_chat_id(message.chat.id)


@dp.callback_query_handler(lambda query: True)
async def callback_handler(query: types.CallbackQuery):
    """Handle callbacks with 'get-task' and 'done' data"""
    if query.data == "get-task":
        await send_task(query.message.chat.id)
    elif query.data == "done":
        await task_done(query.message.chat.id)
    else:
        return


async def send_task(chat_id):
    """Sends a message with the task to user"""
    tasks = taskManager.get_tasks(chat_id)
    task_id, task = random.choice(tasks)
    taskManager.update_done_task_id(task_id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    done_button = types.InlineKeyboardButton(text="Done", callback_data="done")
    get_task_button = types.InlineKeyboardButton(
        text="Get task", callback_data="get-task"
    )
    keyboard.add(done_button, get_task_button)
    await bot.send_message(chat_id, text=task, reply_markup=keyboard)


async def task_done(chat_id):
    """Sends a complete task message to user"""
    keyboard = get_inline_task_keyboard()
    await bot.send_message(
        chat_id, "You are awesome. Do you want a new task?", reply_markup=keyboard,
    )


def get_inline_task_keyboard():
    """Returns inline keyboard"""
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    get_task_button = types.InlineKeyboardButton(
        text="Get task", callback_data="get-task"
    )
    keyboard.add(get_task_button)
    return keyboard


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
