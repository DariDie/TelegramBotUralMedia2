import os, io
import telebot
import logging
import urllib.request as urllib2
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

#Можно сделать текст кнопки эмодзи

@bot.message_handler(commands=['start'])
def start(message):
	#bot.send_message(message.chat.id, "Привет! Пришли мне фото!")
	user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
	user_markup.row('/start', '/stop')
	user_markup.row('1', '2', '3')
	bot.send_message(message.from_user.id, 'Добро пожаловать...', reply_markup=user_markup)

@bot.message_handler(commands=['stop'])
def stop(message):
	hide_markup = telebot.types.ReplyKeyboardHide()
	bot.send_message(message.from_user.id, '..', reply_markup=hide_markup)



@bot.message_handler(content_types=["text"])
def text(message):
	if message.text == '1':
		#url = 'https://drive.google.com/file/d/1d8FGozo0r65SRHDZ7AdKWZVOp87qoe6D/view?usp=sharing'
		#urllib2.urlretrieve(url, 'Синий и Розовый Поддержка Клиентов Блок-Схема.png')
		#img = open('Синий и Розовый Поддержка Клиентов Блок-Схема.png', 'rb')
		img = open('./image/G.jpg')
		bot.send_chat_action(message.from_user.id, 'upload_photo')
		bot.send_photo(message.from_user.id, img)
		img.close()


@server.route("/", methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200


@server.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url=WEBHOOK_URL)
	return "!", 200