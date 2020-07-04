import os, io
import telebot
import logging
from flask import Flask, request


TOKEN = os.environ.get("APIKEY")
WEBHOOK_URL = os.environ.get("MYURL")

bot =telebot.TeleBot(TOKEN)
server = Flask(__name__)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


def get_filer_by_id(file_id):
	file = bot.get_file(file_id)
	downloaded_file = bot.download_file(file.file_path)
	user_photo = io.BytesIO()
	user_photo.write(downloaded_file)
	user_photo.seek(0)
	return user_photo


@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, "Привет! Пришли мне фото!")


@bot.message_handler(content_types=["text"])
def text(message):
	bot.send_message(message.chat.id, "Нет, пришли фото!")


@server.route("/", methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200


@server.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url=WEBHOOK_URL)
	return "!", 200