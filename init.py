import telebot
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("token", "TOKEN")
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    bot.infinity_polling()
