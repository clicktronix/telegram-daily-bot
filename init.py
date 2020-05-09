from os import getenv
from telebot import types
from dotenv import load_dotenv
from telebot import TeleBot

load_dotenv()

token = getenv("token", "TOKEN")
bot = TeleBot(token)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Hello, welcome to the easy routine task bot. \
        We will send simple daily tasks, good luck and \
        enjoyment in their implementation.",
    )
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("Get task"))


if __name__ == "__main__":
    bot.infinity_polling()
